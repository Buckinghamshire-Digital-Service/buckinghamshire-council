import textwrap

from django.test import TestCase

from bs4 import BeautifulSoup
from lxml import etree

from bc.cases.backends.respond.constants import (
    APTEAN_FORM_COMMENT,
    APTEAN_FORM_COMPLAINT,
    APTEAN_FORM_COMPLIMENT,
    APTEAN_FORM_DISCLOSURE,
    APTEAN_FORM_FOI,
    APTEAN_FORM_SAR,
    DESCRIPTION_SCHEMA_NAME,
)
from bc.cases.forms import DisclosureForm
from bc.cases.models import APTEAN_FORM_MAPPING, ApteanRespondCaseFormPage
from bc.home.models import HomePage

from .fixtures import ApteanRespondCaseFormPageFactory


class TestActOfParliamentField(TestCase):
    def test_act_of_parliament_required_for_corresponding_reason(self):
        form_data = {
            "first_name": "Sharon",
            "last_name": "Wattage",
            "contact_method": "E-mail",
            "email": "nightcrawler5@example.com",
            "organisation": "Luton Children's Choir",
            "description": "Please send emergency notes.",
            "investigation": "Operation Forte",
            "reason": [DisclosureForm.ACT_OF_PARLIAMENT],
            "act_of_parliament": "",
        }
        form = DisclosureForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("act_of_parliament" in form.errors)

    def test_appending_act_of_parliament_to_the_description(self):
        form_data = {
            "title": "Inspector",
            "first_name": "Klaus",
            "last_name": "Waffle Iron",
            "contact_method": "E-mail",
            "email": "nightcrawler5@example.com",
            "organisation": "Secret Police",
            "description": "Please send emergency cheese.",
            "investigation": "Operation Crumbly",
            "reason": [DisclosureForm.ACT_OF_PARLIAMENT],
            "act_of_parliament": "State Control of Dairy Goods (Cheese) Act 1998",
        }
        form = DisclosureForm(form_data)
        self.assertTrue(form.is_valid())
        soup = BeautifulSoup(etree.tostring(form.get_xml(form.cleaned_data)), "xml")
        self.assertEqual(
            soup.find(schemaName=DESCRIPTION_SCHEMA_NAME).text,
            textwrap.dedent(
                """\
                Please send emergency cheese.

                What is the investigation?:
                Operation Crumbly

                Why do you need the information?:
                Disclosure is required by an act of Parliament

                The name of the act, the year and the number of the section:
                State Control of Dairy Goods (Cheese) Act 1998"""
            ),
        )

    def test_act_of_parliament_not_appended_when_not_required(self):
        form_data = {
            "first_name": "Royston",
            "last_name": "Carousel",
            "contact_method": "E-mail",
            "email": "fluffybunnyhuns@example.com",
            "organisation": "People's Front of Maidenhead",
            "description": "Please send emergency rabbits.",
            "investigation": "Operation Nibbly",
            "reason": [
                "Without it the prevention or detection of crime will be prejudiced"
            ],
            "act_of_parliament": "",
        }
        form = DisclosureForm(form_data)
        self.assertTrue(form.is_valid())
        soup = BeautifulSoup(etree.tostring(form.get_xml(form.cleaned_data)), "xml")
        self.assertEqual(
            soup.find(schemaName=DESCRIPTION_SCHEMA_NAME).text,
            textwrap.dedent(
                """\
                Please send emergency rabbits.

                What is the investigation?:
                Operation Nibbly

                Why do you need the information?:
                Without it the prevention or detection of crime will be prejudiced"""
            ),
        )


class AttachmentFieldTests(TestCase):

    forms_with_attachments = [
        APTEAN_FORM_COMPLAINT,
        APTEAN_FORM_DISCLOSURE,
        APTEAN_FORM_FOI,
        APTEAN_FORM_SAR,
    ]
    forms_without_attachments = [
        APTEAN_FORM_COMPLIMENT,
        APTEAN_FORM_COMMENT,
    ]
    forms = forms_with_attachments + forms_without_attachments

    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_we_are_testing_all_forms(self):
        for choice, display_name in ApteanRespondCaseFormPage._meta.get_field(
            "form"
        ).choices:
            self.assertIn(choice, self.forms)

    def test_form_consistency(self):
        """Test that the forms we think have file fields do, and vice versa"""

        for form_name in self.forms_with_attachments:
            with self.subTest(form=form_name):
                Form = APTEAN_FORM_MAPPING[form_name]
                self.assertIn("attachments", Form.declared_fields)

        for form_name in self.forms_without_attachments:
            with self.subTest(form=form_name):
                Form = APTEAN_FORM_MAPPING[form_name]
                self.assertNotIn("attachments", Form.declared_fields)

    def test_attachment_form_templates_have_multipart_forms(self):
        for form_name in self.forms_with_attachments:
            with self.subTest(form=form_name):
                self.case_form_page = ApteanRespondCaseFormPageFactory.build(
                    form=form_name
                )
                self.homepage.add_child(instance=self.case_form_page)

                response = self.client.get(self.case_form_page.url)
                soup = BeautifulSoup(response.content.decode())
                form = soup.find("form", class_="form form--standard")
                self.assertIn("enctype", form.attrs)
                self.assertEqual(form.attrs["enctype"], "multipart/form-data")

    def test_data_only_form_templates_have_data_only_forms(self):
        for form_name in self.forms_without_attachments:
            with self.subTest(form=form_name):
                self.case_form_page = ApteanRespondCaseFormPageFactory.build(
                    form=form_name
                )
                self.homepage.add_child(instance=self.case_form_page)

                response = self.client.get(self.case_form_page.url)
                soup = BeautifulSoup(response.content.decode())
                form = soup.find("form", class_="form form--standard")
                self.assertNotIn("enctype", form.attrs)
