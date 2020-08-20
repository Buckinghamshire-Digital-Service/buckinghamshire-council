import textwrap

from django.test import TestCase

from bs4 import BeautifulSoup
from lxml import etree

from bc.cases.backends.respond.constants import DESCRIPTION_SCHEMA_NAME
from bc.cases.forms import DisclosureForm


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
