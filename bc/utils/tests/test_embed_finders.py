from unittest.mock import patch

from django.test import TestCase

from wagtail.embeds import oembed_providers
from wagtail.embeds.finders import get_finders

from bc.utils.embed_finders import YouTubeNoCookieAndRelFinder


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
    @patch("bc.utils.embed_finders.OEmbedFinder.find_embed")
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
    @patch("bc.utils.embed_finders.OEmbedFinder.find_embed")
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
