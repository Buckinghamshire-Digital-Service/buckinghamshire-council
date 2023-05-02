from django.test import SimpleTestCase

from bc.utils.utils import convert_markdown_links_to_html


class TestMarkdownLinksConverter(SimpleTestCase):
    def test_with_markdown_link(self):
        text = "A line with a text and a link [link](www.example.com)"
        expected = (
            'A line with a text and a link <a href="https://www.example.com">link</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_markdown_link_with_http(self):
        text = "A line with a text and a link [link](http://www.example.com)"
        expected = (
            'A line with a text and a link <a href="http://www.example.com">link</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_markdown_link_with_https(self):
        text = "A line with a text and a link [link](https://www.example.com)"
        expected = (
            'A line with a text and a link <a href="https://www.example.com">link</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_markdown_link_with_query_string(self):
        text = "A line with a text and a link [link](www.example.com?query=string)"
        expected = (
            'A line with a text and a link <a href="https://www.example.com?query=string">'
            "link</a>"
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_multiple_markdown_links(self):
        text = "A line with a text and 2 links [link1](www.example.com) and [link2](www.example2.com)"
        expected = (
            'A line with a text and 2 links <a href="https://www.example.com">link1</a> '
            'and <a href="https://www.example2.com">link2</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_float_number(self):
        text = "A line with a text and a link 1.5"
        expected = "A line with a text and a link 1.5"
        self.assertEqual(convert_markdown_links_to_html(text), expected)

    def test_with_ipaddress(self):
        text = "A line with a text and a link [127.0.0.1](127.0.0.1)"
        expected = (
            'A line with a text and a link <a href="https://127.0.0.1">127.0.0.1</a>'
        )
        self.assertEqual(convert_markdown_links_to_html(text), expected)
