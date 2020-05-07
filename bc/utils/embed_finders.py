from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.core.exceptions import ImproperlyConfigured

from wagtail.embeds.finders.oembed import OEmbedFinder
from wagtail.embeds.oembed_providers import youtube

from bs4 import BeautifulSoup


class YouTubeNoCookieAndRelFinder(OEmbedFinder):
    """OEmbed finder to add or preserve the rel=0 parameter and prevent cookies.

    This finder operates on the youtube provider only and adds or preserves the
    source URL rel=0 parameter, if present (because YouTube's OEmbed API
    endpoint strips it from the formatted HTML it returns).

    It also forces the use of the youtube-nocookie.com domain instead of
    youtube.com.
    """

    def __init__(self, providers=None, options=None):
        if providers is None:
            providers = [youtube]

        if providers != [youtube]:
            raise ImproperlyConfigured(
                "The YouTubeNoCookieAndRelFinder only operates on the youtube provider"
            )
        super().__init__(providers=providers, options=options)

    def find_embed(self, url, max_width=None):
        embed = super().find_embed(url, max_width)
        rel = parse_qs(urlparse(url).query).get("rel")
        soup = BeautifulSoup(embed["html"], "html.parser")
        iframe_url = soup.find("iframe").attrs["src"]

        if not (
            iframe_url.startswith("//")
            or iframe_url.startswith("http://")
            or iframe_url.startswith("https://")
        ):
            # apply scheme for urlparse to be able to parse netloc
            iframe_url = "https://" + iframe_url
        scheme, netloc, path, params, query, fragment = urlparse(iframe_url)
        netloc = "www.youtube-nocookie.com"
        querydict = parse_qs(query)
        if rel is None:
            rel = 0
        if querydict.get("rel") != rel:
            querydict["rel"] = rel
        query = urlencode(querydict, doseq=1)
        iframe_url = urlunparse((scheme, netloc, path, params, query, fragment))
        soup.find("iframe").attrs["src"] = iframe_url
        embed["html"] = str(soup)

        return embed
