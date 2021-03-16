import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from bc.utils.blocks import ImageOrEmbedBlock
from bc.home.models import HomePage
from bc.images.tests.fixtures import ImageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory


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
            data={"myblock-image": self.test_image.id}, files={}, prefix="myblock",
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
        struct_value = block.value_from_datadict(data={}, files={}, prefix="myblock",)

        with self.assertRaises(ValidationError):
            block.clean(struct_value)
