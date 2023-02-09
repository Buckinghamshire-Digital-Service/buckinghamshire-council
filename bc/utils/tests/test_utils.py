from django.test import SimpleTestCase

from bc.utils.utils import convert_markdown_links_to_html


class TestMarkdownLinksConverter(SimpleTestCase):
    def test_with_bare_https_link(self):
        text = "A line with a text and a link https://www.example.com"
        expected = 'A line with a text and a link <a href="https://www.example.com">https://www.example.com</a>'
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_bare_http_link(self):
        text = "A line with a text and a link http://www.example.com"
        expected = 'A line with a text and a link <a href="http://www.example.com">http://www.example.com</a>'
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_links_without_protocol(self):
        text = "A line with a text and a link www.example.com"
        expected = 'A line with a text and a link <a href="http://www.example.com">www.example.com</a>'
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_markdown_link(self):
        text = "A line with a text and a link [link](www.example.com)"
        expected = (
            'A line with a text and a link <a href="http://www.example.com">link</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_links_with_query_string(self):
        text = "A line with a text and a link www.example.com?query=string"
        expected = (
            'A line with a text and a link <a href="http://www.example.com?query=string">'
            "www.example.com?query=string</a>"
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)
