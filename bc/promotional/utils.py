from wagtail.models import Site

from .models import PromotionalHomePage


def is_promotional_subsite(site: Site, /) -> bool:
    return isinstance(site.root_page.specific, PromotionalHomePage)
