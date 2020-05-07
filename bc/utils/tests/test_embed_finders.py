from django.test import TestCase
from bc.utils.embed_finders import YouTubeNoCookieAndRelFinder
from unittest.mock import patch
from wagtail.embeds import oembed_providers
from wagtail.embeds.finders import get_finders


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
    def test_youtubenocookieandrelfinder_requests(
        self, mock_find_embed, loads, urlopen
    ):
        mock_find_embed.return_value = {
            "html": '<iframe src="www.youtube.com/watch/123"></iframe>',
            "type": "video",
        }
        result = YouTubeNoCookieAndRelFinder().find_embed(
            "www.youtube.com/watch/123?rel=0"
        )
        self.assertEqual(result["type"], "video")
        self.assertEqual(
            result["html"],
            '<iframe src="https://www.youtube-nocookie.com/watch/123?rel=0"></iframe>',
        )

        # test youtu.be domains
        mock_find_embed.return_value = {
            "html": '<iframe src="https://youtu.be/-wtIMTCHWuI"></iframe>',
            "type": "video",
        }
        result = YouTubeNoCookieAndRelFinder().find_embed("http://youtu.be/-wtIMTCHWuI")
        self.assertEqual(result["type"], "video")
        self.assertEqual(
            result["html"],
            '<iframe src="https://www.youtube-nocookie.com/-wtIMTCHWuI?rel=0"></iframe>',
        )
        # youtub.be with rel parameter
        mock_find_embed.return_value = {
            "html": '<iframe src="https://youtu.be/-wtIMTCHWuI"></iframe>',
            "type": "video",
        }
        result = YouTubeNoCookieAndRelFinder().find_embed(
            "http://youtu.be/-wtIMTCHWuI?rel=0"
        )
        self.assertEqual(result["type"], "video")
        self.assertEqual(
            result["html"],
            '<iframe src="https://www.youtube-nocookie.com/-wtIMTCHWuI?rel=0"></iframe>',
        )
