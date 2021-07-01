from django.test import TestCase

from bc.longform.templatetags.longform_tags import generate_block_number


class BlockNumberTests(TestCase):
    def test_has_chapter_and_heading_numbers(self):
        result = generate_block_number(1, 2, 3, 4)
        self.assertEqual("1.3.4", result)

    def test_has_no_chapter_number(self):
        result = generate_block_number(None, 2, 3, 4)
        self.assertEqual("2.3.4", result)

    def test_has_no_chapter_or_heading_number(self):
        result = generate_block_number(None, None, 3, 4)
        self.assertEqual("3.4", result)

    def test_has_no_subheading_number(self):
        result = generate_block_number(1, 2, None, 4)
        self.assertEqual("1.4", result)

    def test_has_no_paragraph_number(self):
        result = generate_block_number(1, 2, 3, None)
        self.assertEqual("1.3", result)

    def test_has_only_paragraph_number(self):
        result = generate_block_number(None, None, None, 4)
        self.assertEqual("4", result)

    def test_has_no_numbers(self):
        result = generate_block_number(None, None, None, None)
        self.assertEqual("", result)
