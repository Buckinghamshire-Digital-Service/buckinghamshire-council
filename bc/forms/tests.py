from django.core.exceptions import ValidationError
from django.test import TestCase

from bc.forms.fixtures import LookupPageFactory, PostcodeLookupResponseFactory
from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory


class PostcodeLookupResponseTests(TestCase):
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

    def test_postcodes_arrays_are_validated(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["nothing"],
        )
        with self.assertRaises(ValidationError):
            lookup_response.clean_fields()

    def test_postcodes_arrays_are_cleaned(self):
        lookup_response = PostcodeLookupResponseFactory(
            page=self.lookup_page, link_page=self.another_page, postcodes=["HP201UY"],
        )
        lookup_response.clean_fields()
        self.assertEqual(lookup_response.postcodes, ["HP20 1UY"])

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
