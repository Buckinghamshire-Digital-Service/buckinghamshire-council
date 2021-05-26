from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtail.admin.edit_handlers import get_form_for_model

from bc.forms.fixtures import LookupPageFactory, PostcodeLookupResponseFactory
from bc.forms.forms import LookupPageForm
from bc.forms.models import LookupPage
from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory


class PostcodeLookupResponseRequestTests(TestCase):
    def setUp(self):
        homepage = HomePage.objects.first()
        self.lookup_page = LookupPageFactory.build()
        homepage.add_child(instance=self.lookup_page)
        self.another_page = InformationPageFactory.build()
        homepage.add_child(instance=self.another_page)

    def test_initial_page(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP20 1UY"],
        )
        with self.assertTemplateUsed("patterns/pages/forms/lookup_page.html"):
            response = self.client.get(self.lookup_page.url)
        self.assertIn("form", response.context)

    def test_successful_query(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP20 1UY", "W1A 1AA"],
        )

        with self.assertTemplateUsed("patterns/pages/forms/lookup_page_landing.html"):
            response = self.client.get(self.lookup_page.url + "?postcode=HP20+1UY")
        self.assertEqual(response.context["lookup_response"], lookup_response)

    def test_query_not_found(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP20 1UY"],
        )

        with self.assertTemplateUsed("patterns/pages/forms/lookup_page.html"):
            response = self.client.get(self.lookup_page.url + "?postcode=W1A+1AA")
        self.assertEqual(
            response.context["form"]["postcode"].errors[0],
            self.lookup_page.no_match_message,
        )

    def test_multiple_hits_error(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP20 1UY"],
        )
        PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP20 1UY"],
        )

        with self.assertTemplateUsed("patterns/pages/forms/lookup_page.html"):
            response = self.client.get(self.lookup_page.url + "?postcode=HP20+1UY")
        self.assertEqual(
            response.context["form"]["postcode"].errors[0],
            "Sorry, an error occured. This has been reported.",
        )

    def test_postcodes_are_cleaned_on_search_input(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP201UY"],
        )

        form = self.lookup_page.get_form({"postcode": "hp201uy"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["postcode"], "HP20 1UY")

    def test_formatting_answer(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            answer="The postcode {postcode} is what you submitted.",
        )
        lookup_response.queried_postcode = "HP20 1UY"
        self.assertEqual(
            lookup_response.format_answer(),
            "The postcode HP20 1UY is what you submitted.",
        )


class PostcodeLookupResponseAdminTests(TestCase):
    def setUp(self):
        homepage = HomePage.objects.first()
        self.lookup_page = LookupPageFactory.build()
        homepage.add_child(instance=self.lookup_page)
        self.another_page = InformationPageFactory.build()
        homepage.add_child(instance=self.another_page)

    def get_page_form_data(self, updates):
        data = {
            "form_heading": '{"blocks":[{"key":"1dnij","text":"Look up a postcode",'
            '"type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],'
            '"data":{}}],"entityMap":{}}',
            "input_help_text": "Test",
            "input_label": "Enter a postcode",
            "no_match_message": "No match",
            "responses-INITIAL_FORMS": "1",
            "slug": "duplicate-postcodes-test-page",
            "start_again_text": "Have another go, because this is so fun.",
            "title": "Duplicate postcodes test page",
        }
        data.update(updates)
        return data

    @staticmethod
    def response_data(*, i: int, postcodes: str, **kwargs: str) -> dict:
        prefix = f"responses-{i}-"
        data = {
            "DELETE": kwargs.get("DELETE", ""),
            "answer": kwargs.get("answer", "some answer"),
            "id": "",
            "link_button_text": "",
            "link_page": "3",
            "postcodes": postcodes,
        }
        return {prefix + key: value for key, value in data.items()}

    def test_postcodes_arrays_are_validated(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="nothing"),
                "responses-TOTAL_FORMS": "1",
            }
        )

        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.formsets["responses"][0].errors["postcodes"], ["Invalid Postcode"]
        )

    def test_postcodes_arrays_are_cleaned(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="HP201UY"),
                "responses-TOTAL_FORMS": "1",
            }
        )

        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.formsets["responses"][0].cleaned_data["postcodes"], ["HP20 1UY"]
        )

    def test_valid_postcode_wildcard(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            answer="This includes {postcode}, which is valid.",
        )
        try:
            lookup_response.clean_fields()
        except ValidationError:
            self.fail("Including {postcode} in the answer failed validation")

    def test_invalid_postcode_wildcard(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            answer="This includes an invalid {wildcard}.",
        )
        with self.assertRaises(ValidationError):
            lookup_response.clean_fields()

    def test_detecting_duplicate_postcodes(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="W1A 1AA, SW1A 1AA, BX4 7SB"),
                **self.response_data(
                    i=1, postcodes="DH99 1NS, DE99 3GG, XM4 5HQ, W1A 1AA"
                ),
                "responses-TOTAL_FORMS": "2",
            }
        )

        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"],
            ["The postcode W1A 1AA appears in multiple responses"],
        )

    def test_detecting_duplicate_postcodes_with_different_formatting(self):
        """E.g. W1A 1AA and W1A1AA should be treated as equal"""
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="W1A 1AA, SW1A 1AA"),
                **self.response_data(i=1, postcodes="DH99 1NS, W1A1AA"),
                "responses-TOTAL_FORMS": "2",
            }
        )

        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"],
            ["The postcode W1A 1AA appears in multiple responses"],
        )

    def test_detecting_multiple_duplicate_postcodes(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="W1A 1AA, SW1A 1AA, BX4 7SB"),
                **self.response_data(
                    i=1, postcodes="DH99 1NS, DE99 3GG, XM4 5HQ, SW1A 1AA, W1A 1AA"
                ),
                "responses-TOTAL_FORMS": "2",
            }
        )

        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            form.errors["__all__"],
            [
                # We don't sort the error message, because it might be long
                ["The postcodes SW1A 1AA, W1A 1AA appear in multiple responses"],
                ["The postcodes W1A 1AA, SW1A 1AA appear in multiple responses"],
            ],
        )

    def test_detecting_duplicate_postcodes_across_multiple_entries(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="W1A 1AA, SW1A 1AA"),
                **self.response_data(i=1, postcodes="DH99 1NS, DE99 3GG"),
                **self.response_data(i=2, postcodes="XM4 5HQ, E17 1AA"),
                **self.response_data(i=3, postcodes="N1 1AA"),
                **self.response_data(i=4, postcodes="EH99 1SP, G58 1SB"),
                **self.response_data(i=5, postcodes="BX4 7SB, E17 1AA"),
                **self.response_data(i=6, postcodes="SW1A 2AA, XM4 5HQ"),
                "responses-TOTAL_FORMS": "7",
            }
        )
        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            form.errors["__all__"],
            [
                # We don't sort the error message, because it might be long
                ["The postcodes E17 1AA, XM4 5HQ appear in multiple responses"],
                ["The postcodes XM4 5HQ, E17 1AA appear in multiple responses"],
            ],
        )

    def test_duplicate_postcodes_in_deleted_formset_forms_are_ignored(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="W1A 1AA, SW1A 1AA"),
                **self.response_data(i=1, postcodes="GIR 0AA, W1A 1AA", DELETE="1"),
                "responses-TOTAL_FORMS": "2",
            }
        )
        MyLookupPageForm = get_form_for_model(LookupPage, form_class=LookupPageForm)
        form = MyLookupPageForm(data)
        self.assertTrue(form.is_valid())
