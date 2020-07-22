from unittest.mock import patch

from django.test import TestCase

from wagtail.embeds import oembed_providers
from wagtail.embeds.finders import get_finders

from bs4 import BeautifulSoup

from bc.utils.embed_finders import CustomOEmbedFinder, YouTubeNoCookieAndRelFinder


class YouTubeNoCookieAndRelFinderTest(TestCase):
    def test_defaults_to_oembed(self):
        finders = get_finders()

        self.assertEqual(len(finders), 2)
        self.assertIsInstance(finders[0], YouTubeNoCookieAndRelFinder)

    def test_youtubenocookieandrelfinder_accepts_known_provider(self):
        finder = YouTubeNoCookieAndRelFinder(providers=[oembed_providers.youtube])
        self.assertTrue(finder.accept("http://www.youtube.com/watch/"))
        self.assertTrue(finder.accept("http://youtu.be/-wtIMTCHWuI"))
        self.assertTrue(finder.accept("http://youtu.be/-wtIMTCHWuI?rel=0"))
        self.assertFalse(finder.accept("https://twitter.com/pydatabristol"))

    @patch("urllib.request.urlopen")
    @patch("json.loads")
    @patch("bc.utils.embed_finders.CustomOEmbedFinder.find_embed")
    def test_plain_youtube_domain(self, mock_find_embed, loads, urlopen):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.youtube.com/watch/123"></iframe>',
            "type": "video",
        }

        # test with and without ?rel=0 parameter
        for input_url in [
            "www.youtube.com/watch/123",
            "www.youtube.com/watch/123?rel=0",
        ]:
            with self.subTest(input_url=input_url):
                result = YouTubeNoCookieAndRelFinder().find_embed(
                    "www.youtube.com/watch/123?rel=0"
                )
                self.assertEqual(result["type"], "video")
                self.assertEqual(
                    result["html"],
                    '<iframe src="https://www.youtube-nocookie.com/watch/123?rel=0"></iframe>',
                )

    @patch("urllib.request.urlopen")
    @patch("json.loads")
    @patch("bc.utils.embed_finders.CustomOEmbedFinder.find_embed")
    def test_dot_be_domain(self, mock_find_embed, loads, urlopen):
        mock_find_embed.return_value = {
            "html": '<iframe src="https://youtu.be/-wtIMTCHWuI"></iframe>',
            "type": "video",
        }

        # test with and without ?rel=0 parameter
        for input_url in [
            "http://youtu.be/-wtIMTCHWuI",
            "http://youtu.be/-wtIMTCHWuI?rel=0",
        ]:
            with self.subTest(input_url=input_url):
                result = YouTubeNoCookieAndRelFinder().find_embed(input_url)
                self.assertEqual(result["type"], "video")
                self.assertEqual(
                    result["html"],
                    '<iframe src="https://www.youtube-nocookie.com/-wtIMTCHWuI?rel=0"></iframe>',
                )


@patch("bc.utils.embed_finders.OEmbedFinder.find_embed")
class CustomOEmbedFinderTest(TestCase):
    def test_video_iframe_classes(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_classes = ["video_iframe_class"]
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        self.assertEqual(soup.find("iframe").attrs.get("class"), ["video_iframe_class"])

    def test_nonvideo_iframe_classes(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "not a video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_classes = ["video_iframe_class"]
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        self.assertEqual(soup.find("iframe").attrs.get("class"), None)

    def test_video_wrapper_classes(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_wrapper_classes = ["video_wrapper_class"]
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        self.assertEqual(soup.find("div").attrs.get("class"), ["video_wrapper_class"])

    def test_nonvideo_wrapper_classes(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "not a video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_wrapper_classes = ["video_wrapper_class"]
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        self.assertEqual(soup.find("div"), None)

    def test_video_wrapper_wraps_iframe(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "video",
        }

        finder = CustomOEmbedFinder()
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        self.assertEqual(soup.find("iframe").parent.name, "div")

    def test_nonvideo_gets_no_wrapper(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "not a video",
        }

        finder = CustomOEmbedFinder()
        result = finder.find_embed("www.example.com")
        soup = BeautifulSoup(result["html"], "html.parser")
        # it is at the top level
        self.assertEqual(soup.find("iframe").parent.name, "[document]")

    def test_video_output_html(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_classes = ["foo", "bar"]
        finder.extra_wrapper_classes = ["baz", "qux"]
        result = finder.find_embed("www.example.com")
        self.assertEqual(
            result["html"],
            '<div class="baz qux"><iframe class="foo bar" src="www.example.com"></iframe></div>',
        )

    def test_nonvideo_output_html(self, mock_find_embed):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.example.com"></iframe>',
            "type": "not a video",
        }

        finder = CustomOEmbedFinder()
        finder.extra_classes = ["foo", "bar"]
        finder.extra_wrapper_classes = ["baz", "qux"]
        result = finder.find_embed("www.example.com")
        self.assertEqual(
            result["html"], '<iframe src="www.example.com"></iframe>',
        )
