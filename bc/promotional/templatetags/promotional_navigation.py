import logging

from django import template
from django.core.cache import cache

from wagtail.models import Site

from .. import utils
from ..navigation import PrimaryNavigation

logger = logging.getLogger(__name__)

register = template.Library()


# Promotional primary navigation
@register.inclusion_tag(
    "patterns/organisms/header-navigation/header-navigation.html", takes_context=True
)
def promotional_primary_navigation(context):
    request = context["request"]
    current_site = Site.find_for_request(request)
    try:
        site_config = utils.get_promotional_site_configuration(current_site)
    except utils.PromotionalSiteConfigurationDoesNotExist:
        logger.exception(
            "Failed to get promotional site configuration for site_pk=%s.",
            current_site.pk,
        )
        return {"items": []}
    nav = PrimaryNavigation(
        site_config=site_config,
        site=current_site,
        cache=cache,
    )
    return {"items": nav.fetch_navigation_items(current_path=request.path)}
