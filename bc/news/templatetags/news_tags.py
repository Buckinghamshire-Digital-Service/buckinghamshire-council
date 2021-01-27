from django import template

from bc.news.models import NewsPage

register = template.Library()


@register.filter
def is_news_page(page):
    """Return True if page is a news page."""
    return isinstance(page, NewsPage)
