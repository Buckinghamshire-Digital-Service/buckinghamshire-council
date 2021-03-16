from django.test import TestCase
from django.core.exceptions import ValidationError

from bc.campaigns.blocks import ImageOrEmbedBlock


class TestImageOrEmbedBlock(TestCase):
    def test_adding_only_image_works(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={"myblock-image": 1}, files={}, prefix="myblock",
        )

        block.clean(struct_value)

        # Test will fail if raises unexpected error

    def test_adding_only_embed_works(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={"myblock-embed": "https://youtu.be/ahcmNsNjQUw"},
            files={},
            prefix="myblock",
        )

        block.clean(struct_value)

        # Test will fail if raises unexpected error

    def test_adding_both_throws_error(self):
        block = ImageOrEmbedBlock()
        struct_value = block.value_from_datadict(
            data={"myblock-image": 1, "myblock-embed": "https://youtu.be/ahcmNsNjQUw"},
            files={},
            prefix="myblock",
        )

        with self.assertRaises(ValidationError):
            block.clean(struct_value)
