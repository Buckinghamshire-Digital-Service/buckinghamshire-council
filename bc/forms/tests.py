from unittest.mock import patch

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from wagtail.admin.panels import get_form_for_model

from bs4 import BeautifulSoup
from freezegun import freeze_time

from bc.forms.fixtures import LookupPageFactory, PostcodeLookupResponseFactory
from bc.forms.forms import LookupPageForm
from bc.forms.models import (
    FormField,
    FormPage,
    FormSubmission,
    FormSubmissionAccessControl,
    LookupPage,
)
from bc.home.models import HomePage
from bc.standardpages.models import InformationPage
from bc.standardpages.tests.fixtures import InformationPageFactory
from bc.users.models import User

DISABLE_RECAPTCHA = patch("django_recaptcha.fields.ReCaptchaField.validate")


class PostcodeLookupResponseRequestTests(TestCase):
    def setUp(self):
        homepage = HomePage.objects.first()
        self.lookup_page = LookupPageFactory.build()
        homepage.add_child(instance=self.lookup_page)
        self.another_page = InformationPageFactory.build()
        homepage.add_child(instance=self.another_page)

    def test_initial_page(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP20 1UY"],
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
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP20 1UY"],
        )

        with self.assertTemplateUsed("patterns/pages/forms/lookup_page.html"):
            response = self.client.get(self.lookup_page.url + "?postcode=W1A+1AA")
        self.assertEqual(
            response.context["form"]["postcode"].errors[0],
            self.lookup_page.no_match_message,
        )

    def test_multiple_hits_error(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP20 1UY"],
        )
        PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP20 1UY"],
        )

        with self.assertTemplateUsed("patterns/pages/forms/lookup_page.html"):
            response = self.client.get(self.lookup_page.url + "?postcode=HP20+1UY")
        self.assertEqual(
            response.context["form"]["postcode"].errors[0],
            "Sorry, an error occured. This has been reported.",
        )

    def test_postcodes_are_cleaned_on_search_input(self):
        PostcodeLookupResponseFactory(
            page=self.lookup_page,
            link_page=self.another_page,
            postcodes=["HP201UY"],
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
                **self.response_data(i=1, postcodes="HP201UY, "),
                **self.response_data(i=2, postcodes=", E17 1AA"),
                **self.response_data(i=3, postcodes=""),
                **self.response_data(i=4, postcodes=","),
                "responses-TOTAL_FORMS": "5",
            }
        )

        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
        form = MyLookupPageForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.formsets["responses"][0].errors["postcodes"], ["Invalid Postcode"]
        )
        self.assertEqual(
            form.formsets["responses"][1].errors["postcodes"],
            ["Item 2 in the array did not validate: This field is required."],
        )
        self.assertEqual(
            form.formsets["responses"][2].errors["postcodes"],
            ["Item 1 in the array did not validate: This field is required."],
        )
        self.assertEqual(
            form.formsets["responses"][3].errors["postcodes"],
            ["This field is required."],
        )
        self.assertEqual(
            form.formsets["responses"][4].errors["postcodes"],
            [
                "Item 1 in the array did not validate: This field is required.",
                "Item 2 in the array did not validate: This field is required.",
            ],
        )

    def test_postcodes_arrays_are_cleaned(self):
        data = self.get_page_form_data(
            {
                **self.response_data(i=0, postcodes="HP201UY"),
                "responses-TOTAL_FORMS": "1",
            }
        )

        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
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

        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
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

        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
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

        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
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
        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
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
        MyLookupPageForm = get_form_for_model(
            LookupPage, form_class=LookupPageForm, formsets=["responses"]
        )
        form = MyLookupPageForm(data)
        self.assertTrue(form.is_valid())


class SubmissionAutoDeletionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        homepage = HomePage.objects.first()
        cls.form_page = homepage.add_child(
            instance=FormPage(
                title="Test form",
                slug="test-form",
                listing_summary="Test form",
                auto_delete=7,
            )
        )
        # create submissions with different `submit_time` values
        cls.submissions = []
        for timestamp in [
            "2025-01-01 12:00:00+00:00",
            "2025-01-03 12:00:00+00:00",
            "2025-01-05 12:00:00+00:00",
        ]:
            submission = cls.form_page.formsubmission_set.create(form_data={})
            submission.submit_time = timestamp
            submission.save(update_fields=["submit_time"])
            cls.submissions.append(submission)

    @freeze_time("2024-01-01 12:00:00")  # a year before
    def test_submissions_in_future(self):
        self.assertQuerySetEqual(FormSubmission.objects.stale(), [])

    @freeze_time("2026-01-01 12:00:00")  # a year after
    def test_submissions_all_stale(self):
        self.assertQuerySetEqual(
            FormSubmission.objects.stale(), self.submissions, ordered=False
        )

    @freeze_time("2025-01-09 12:00:00")  # 8 days after the first submission
    def test_submissions_partial_stale(self):
        self.assertQuerySetEqual(FormSubmission.objects.stale(), self.submissions[:1])

    @freeze_time("2025-01-10 10:00:00")  # exactly 7 days after the second submission
    def test_submissions_partial_stale_same_day(self):
        self.assertQuerySetEqual(FormSubmission.objects.stale(), self.submissions[:1])

    @freeze_time("2026-01-01 12:00:00")
    def test_command_is_safe_by_default(self):
        call_command("stale_submissions")
        self.assertQuerySetEqual(
            FormSubmission.objects.all(), self.submissions, ordered=False
        )

    @freeze_time("2026-01-01 12:00:00")
    def test_command_deletion(self):
        call_command("stale_submissions", delete=True)
        self.assertQuerySetEqual(FormSubmission.objects.all(), [])


class FormSubmissionAccessControlTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        homepage = HomePage.objects.first()
        cls.form_page = homepage.add_child(
            instance=FormPage(
                title="Test form",
                slug="test-form",
                listing_summary="Test form",
            )
        )
        FormField.objects.create(
            page=cls.form_page,
            label="Name",
            field_type="singleline",
            required=True,
        )
        cls.form_page.formsubmission_set.create(form_data={"name": "Test Name"})
        cls.submissions_url = reverse(
            "wagtailforms:list_submissions", args=(cls.form_page.pk,)
        )

        editor_group = Group.objects.get(name="Editors")
        access_group = Group.objects.create(name="Access")
        no_access_group = Group.objects.create(name="No access")

        cls.access_control = FormSubmissionAccessControl.load()
        cls.access_control.groups_with_access.add(access_group)

        cls.users = {
            "superuser": User.objects.create_superuser(username="superuser"),
            "access": User.objects.create(username="access"),
            "noaccess": User.objects.create(username="noaccess"),
        }
        cls.users["access"].groups.add(editor_group, access_group)
        cls.users["noaccess"].groups.add(editor_group, no_access_group)

    def test_superuser(self):
        self.client.force_login(self.users["superuser"])
        response = self.client.get(self.submissions_url)
        self.assertContains(response, "<td>Test Name</td>", html=True)

    def test_user_with_access(self):
        self.client.force_login(self.users["access"])
        response = self.client.get(self.submissions_url)
        self.assertContains(response, "<td>Test Name</td>", html=True)

    def test_user_with_no_access(self):
        self.client.force_login(self.users["noaccess"])
        response = self.client.get(self.submissions_url)
        self.assertRedirects(response, "/admin/")


class EmbeddedFormBlockTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        homepage = HomePage.objects.first()
        cls.form_page = homepage.add_child(
            instance=FormPage(
                title="Test form",
                slug="test-form",
                listing_summary="Test form",
                thank_you_heading="Test thank you heading",
                thank_you_text="Test thank you text",
            )
        )
        cls.info_page = homepage.add_child(
            instance=InformationPage(
                title="Test page",
                slug="test-page",
                listing_summary="Test page",
                body=[("form", cls.form_page)],
            )
        )
        FormField.objects.create(
            page=cls.form_page,
            sort_order=1,
            label="Your email",
            field_type="email",
            required=True,
        )
        FormField.objects.create(
            page=cls.form_page,
            sort_order=2,
            label="Your message",
            field_type="multiline",
            required=True,
            help_text="<em>please</em> be polite",
        )
        FormField.objects.create(
            page=cls.form_page,
            sort_order=3,
            label="Your choices",
            field_type="checkboxes",
            required=False,
            choices="foo,bar,baz",
        )

    def test_embed(self):
        response = self.client.get(self.info_page.url)

        # using beautifulsoup instead of assertContains() because of the
        # auto-generated id of embedded form elements
        soup = BeautifulSoup(response.content)
        soup.find_all()
        self.assertIsNotNone(
            soup.find("input", attrs={"type": "email", "name": "your_email"}),
        )
        self.assertIsNotNone(
            soup.find("textarea", attrs={"name": "your_message"}), msg="<textarea name"
        )
        self.assertIsNotNone(
            soup.find(
                "input",
                attrs={"type": "checkbox", "name": "your_choices", "value": "baz"},
            )
        )

        self.assertContains(
            response,
            '<input class="form__submit button" type="submit" value="Submit" />',
        )

    def test_field_additional_text_rendered(self):
        self.form_page.form_fields.filter(field_type="email").update(
            additional_text="<p>test additional text</p>"
        )
        response = self.client.get(self.info_page.url)
        self.assertContains(response, "<p>test additional text</p>", html=True)

    def test_page_introduction_rendered(self):
        self.form_page.introduction = "Test introduction"
        self.form_page.save(update_fields=["introduction"])
        response = self.client.get(self.info_page.url)
        self.assertContains(response, "Test introduction")

    def test_page_action_text_rendered(self):
        self.form_page.action_text = "TESTSAVE"
        self.form_page.save(update_fields=["action_text"])
        response = self.client.get(self.info_page.url)
        self.assertContains(
            response,
            '<input class="form__submit button" type="submit" value="TESTSAVE" />',
        )

    def test_embed_multiple(self):
        self.info_page.body = [("form", self.form_page), ("form", self.form_page)]
        self.info_page.save(update_fields=["body"])
        response = self.client.get(self.info_page.url)
        soup = BeautifulSoup(response.content)
        # The multiple assignment also tests that there are exactly two inputs
        input1, input2 = soup.find_all("input", attrs={"name": "your_email"})
        self.assertNotEqual(input1.attrs["id"], input2.attrs["id"])

    def test_embed_hidden_fields(self):
        response = self.client.get(self.info_page.url)
        soup = BeautifulSoup(response.content)
        form = soup.find(
            lambda tag: (
                tag.name == "form"
                and tag.find_parent(attrs={"class": "embedded-form"}) is not None
            )
        )

        embed_id = form.find("input", attrs={"name": "embed_id"}).attrs["value"]
        embed_form_id = form.find("input", attrs={"name": "embed_form_id"}).attrs[
            "value"
        ]

        self.assertEqual(embed_id, str(self.info_page.pk))
        self.assertEqual(embed_form_id, "test-form_1")

    def test_embed_form_has_h2_with_id(self):
        response = self.client.get(self.info_page.url)
        soup = BeautifulSoup(response.content)
        h2 = soup.find("h2", attrs={"id": "test-form_1"})
        self.assertIsNotNone(h2, 'Couldn\'t find <h2 id="test-form_1">')
        self.assertEqual(h2.text, "Test form")

    @DISABLE_RECAPTCHA
    def test_embed_submission(self, mocked_validate):
        data = {
            "your_email": "test@example.com",
            "your_message": "test",
            "embed_id": self.info_page.pk,
            "embed_form_id": "test-form_1",
        }
        response = self.client.post(self.form_page.url, data=data, follow=True)
        self.assertRedirects(
            response, "/test-page/?embed_success=test-form_1#test-form_1"
        )
        self.assertContains(response, "Test thank you text")
        self.assertContains(
            response,
            '<h3 class="form__success--heading">Test thank you heading</h3>',
            html=True,
        )

    @DISABLE_RECAPTCHA
    def test_embed_invalid(self, mocked_validate):
        data = {
            "your_email": "",  # required field
            "your_message": "test",
            "embed_id": self.info_page.pk,
            "embed_form_id": "test-form_1",
        }
        response = self.client.post(self.form_page.url, data=data)
        soup = BeautifulSoup(response.content)
        form = soup.find("form", attrs={"class": "form form--standard"})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "your_email", "This field is required."
        )

        embed_id = form.find("input", attrs={"name": "embed_id"}).attrs["value"]
        embed_form_id = form.find("input", attrs={"name": "embed_form_id"}).attrs[
            "value"
        ]

        self.assertEqual(embed_id, str(self.info_page.pk))
        self.assertEqual(embed_form_id, "test-form_1")
