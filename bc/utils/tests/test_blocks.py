import json

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.test import TestCase

from bc.home.models import HomePage
from bc.images.tests.fixtures import ImageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory
from bc.utils.blocks import BaseChartBlock, ImageOrEmbedBlock


class TestChartBlock(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_clean_table_values(self):
        table = [
            ["Row 1, Col 1", " ", "Row 1, Col 2", None, "Row 1, Col 3"],
            [None, " ", None, None, None],
            ["Row 2, Col 1", " ", "Row 2, Col 2", None, "Row 2, Col 3"],
            ["Row 3, Col 1", " ", "Row 3, Col 2", None, "Row 3, Col 3"],
            ["Row 4, Col 1", " ", "Row 4, Col 2", None, "Row 4, Col 3"],
        ]

        result = BaseChartBlock.clean_table_values(None, table)

        # Result should be the same table but without any empty rows or columns
        self.assertEqual(
            [
                ["Row 1, Col 1", "Row 1, Col 2", "Row 1, Col 3"],
                ["Row 2, Col 1", "Row 2, Col 2", "Row 2, Col 3"],
                ["Row 3, Col 1", "Row 3, Col 2", "Row 3, Col 3"],
                ["Row 4, Col 1", "Row 4, Col 2", "Row 4, Col 3"],
            ],
            result,
        )

    def test_convert_column_data_to_numbers(self):
        list_of_columns = [
            # Column of alphanumeric strings
            {"name": "Column 1", "data": ["Data 1", "Data 2", "Data 3"]},
            # Column of numeric strings
            {"name": "Column 2", "data": ["1", "2.0", "3.4"]},
            # Column of a mix of alphanumeric and numeric strings
            {"name": "Column 2", "data": ["Data 4", "5.6", "Data 7"]},
        ]

        result = BaseChartBlock.convert_column_data_to_numbers(None, list_of_columns)

        # Column name is unchanged, order is unchanged
        self.assertEqual(list_of_columns[0]["name"], result[0]["name"])
        self.assertEqual(list_of_columns[1]["name"], result[1]["name"])
        self.assertEqual(list_of_columns[2]["name"], result[2]["name"])

        # Alphanumeric strings stay the same
        self.assertEqual(list_of_columns[0]["data"], result[0]["data"])

        # Numeric strings are converted to floats
        self.assertEqual([1.0, 2.0, 3.4], result[1]["data"])

        # Alphanumeric strings stay the same and numeric strings are converted to floats
        self.assertEqual(["Data 4", 5.6, "Data 7"], result[2]["data"])

    def test_get_table_columns(self):
        table = [
            ["Row 1, Col 1", "Row 1, Col 2", "Row 1, Col 3"],
            ["Row 2, Col 1", "Row 2, Col 2", "Row 2, Col 3"],
            ["Row 3, Col 1", "Row 3, Col 2", "Row 3, Col 3"],
        ]

        result = BaseChartBlock.get_table_columns(None, table)

        # Result should be a list of column dictionaries with the first row
        # as column headings
        self.assertEqual(
            [
                {"name": "Row 1, Col 1", "data": ["Row 2, Col 1", "Row 3, Col 1"]},
                {"name": "Row 1, Col 2", "data": ["Row 2, Col 2", "Row 3, Col 2"]},
                {"name": "Row 1, Col 3", "data": ["Row 2, Col 3", "Row 3, Col 3"]},
            ],
            result,
        )


class TestStreamfieldHeadingTemplates(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_heading_uses_heading_template(self):
        page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                body=json.dumps(
                    [
                        {
                            "type": "heading",
                            "value": "I should use the heading_block.html template",
                        }
                    ]
                )
            )
        )
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "patterns/molecules/streamfield/blocks/heading_block.html"
        )

        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/subheading_block.html"
        )
        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/subsubheading_block.html"
        )

    def test_subheading_uses_subheading_template(self):
        page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                body=json.dumps(
                    [
                        {
                            "type": "subheading",
                            "value": "I should use the subheading_block.html template",
                        }
                    ]
                )
            )
        )
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "patterns/molecules/streamfield/blocks/subheading_block.html"
        )

        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/heading_block.html"
        )
        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/subsubheading_block.html"
        )

    def test_heading_within_accordion_uses_subheading_template(self):
        page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                body=json.dumps(
                    [
                        {
                            "type": "accordion",
                            "value": {
                                "items": [
                                    {
                                        "content": [
                                            {
                                                "type": "heading",
                                                "value": "Being inside an accordion, "
                                                "with its own h2 title, I should use "
                                                "subheading_block.html",
                                            },
                                        ]
                                    }
                                ]
                            },
                        }
                    ]
                )
            )
        )
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "patterns/molecules/streamfield/blocks/subheading_block.html"
        )

        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/heading_block.html"
        )
        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/subsubheading_block.html"
        )

    def test_subheading_within_accordion_uses_subsubheading_template(self):
        page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                body=json.dumps(
                    [
                        {
                            "type": "accordion",
                            "value": {
                                "items": [
                                    {
                                        "content": [
                                            {
                                                "type": "subheading",
                                                "value": "Being inside an accordion, "
                                                "with its own h2 title, I should use "
                                                "subsubheading_block.html",
                                            },
                                        ]
                                    }
                                ]
                            },
                        }
                    ]
                )
            )
        )
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "patterns/molecules/streamfield/blocks/subsubheading_block.html"
        )

        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/heading_block.html"
        )
        self.assertTemplateNotUsed(
            response, "patterns/molecules/streamfield/blocks/subheading_block.html"
        )


class TestImageOrEmbedBlock(TestCase):
    def setUp(self):
        self.test_image = ImageFactory.create()
        self.test_image.refresh_from_db()

    def test_adding_only_image_works(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={"myblock-image": self.test_image.id},
            files={},
            prefix="myblock",
        )

        cleaned_value = block.clean(struct_value)

        self.assertIsNotNone(cleaned_value["image"])

    def test_adding_only_embed_works(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={"myblock-embed": "https://youtu.be/ahcmNsNjQUw"},
            files={},
            prefix="myblock",
        )

        cleaned_value = block.clean(struct_value)

        self.assertIsNotNone(cleaned_value["embed"])

    def test_adding_both_throws_error(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={
                "myblock-image": self.test_image.id,
                "myblock-embed": "https://youtu.be/ahcmNsNjQUw",
            },
            files={},
            prefix="myblock",
        )

        with self.assertRaises(ValidationError):
            block.clean(struct_value)

    def test_adding_neither_throws_error(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={},
            files={},
            prefix="myblock",
        )

        with self.assertRaises(ValidationError):
            block.clean(struct_value)


class TestAccordionTemplate(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_aria_controls_attribute(self):
        page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                body=json.dumps(
                    [
                        {
                            "type": "accordion",
                            "value": {
                                "items": [
                                    {
                                        "title": "Question 1",
                                        "content": [
                                            {"type": "paragraph", "value": "Answer 1"},
                                        ],
                                    },
                                    {
                                        "title": "Question 2",
                                        "content": [
                                            {"type": "paragraph", "value": "Answer 2"},
                                        ],
                                    },
                                ]
                            },
                        }
                    ]
                )
            )
        )
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patterns/molecules/accordion/accordion.html")
        soup = BeautifulSoup(response.content, "html.parser")

        accordions = soup.find_all("div", class_="accordion")
        for accordion in accordions:
            button = accordion.find("button", class_="accordion__button")
            answer = accordion.find("div", class_="accordion__content")

            with self.subTest("The button controls the answer"):
                self.assertEqual(button.attrs["aria-controls"], answer.attrs["id"])
            with self.subTest("The answer is labelled by the button"):
                self.assertEqual(button.attrs["id"], answer.attrs["aria-labelledby"])

        with self.subTest("There are two accordions"):
            self.assertEqual(len(accordions), 2)

        with self.subTest("accordion IDs are unique"):
            question_ids = {
                el.attrs["id"]
                for el in soup.find_all("button", class_="accordion__button")
            }
            self.assertEqual(len(question_ids), 2)

            answer_ids = {
                el.attrs["id"]
                for el in soup.find_all("div", class_="accordion__content")
            }
            self.assertEqual(len(answer_ids), 2)
