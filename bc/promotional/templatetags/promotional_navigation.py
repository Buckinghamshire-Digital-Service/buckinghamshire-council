import logging
from typing import Optional, Sequence, TypedDict

from django import template
from django.core.cache import cache

from wagtail.models import Site

from .. import utils
from ..models import PromotionalSiteConfiguration
from ..navigation import PrimaryNavigation, PrimaryNavigationItem

logger = logging.getLogger(__name__)

register = template.Library()


class CTALink(TypedDict):
    url: str
    text: str


class PrimaryNavigationContext(TypedDict):
    items: Sequence[PrimaryNavigationItem]
    primary_cta: Optional[CTALink]


def _primary_nav_items(
    *, config: PromotionalSiteConfiguration, site: Site, current_path: str
) -> Sequence[PrimaryNavigationItem]:
    nav = PrimaryNavigation(
        site_config=config,
        site=site,
        cache=cache,
    )
    return nav.fetch_navigation_items(current_path=current_path)


def _primary_cta_item(
    *, config: PromotionalSiteConfiguration, site: Site
) -> Optional[CTALink]:
    if config.primary_cta_link_page is not None:
        return {
            "url": config.primary_cta_link_page.get_url(current_site=site),
            "text": config.primary_cta_link_text or config.primary_cta_link_page.title,
        }
    return None


# Promotional primary navigation
@register.inclusion_tag(
    "patterns/organisms/header-navigation/header-navigation.html", takes_context=True
)
def promotional_primary_navigation(context) -> PrimaryNavigationContext:
    request = context["request"]
    current_site = Site.find_for_request(request)

    try:
        site_config = utils.get_promotional_site_configuration(current_site)
    except utils.PromotionalSiteConfigurationDoesNotExist:
        logger.exception(
            "Failed to get promotional site configuration for site_pk=%s.",
            current_site.pk,
        )
        return {"items": [], "primary_cta": None}

    return {
        "items": _primary_nav_items(
            config=site_config, site=current_site, current_path=request.path
        ),
        "primary_cta": _primary_cta_item(config=site_config, site=current_site),
    }
