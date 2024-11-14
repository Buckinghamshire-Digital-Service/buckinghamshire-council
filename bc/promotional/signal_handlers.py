import logging

from django.core.cache import cache
from django.db.models import Model

from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.models import Page
from wagtail.signals import page_published, page_unpublished

from . import utils
from .models import PromotionalSiteConfiguration
from .navigation import PrimaryNavigation

logger = logging.getLogger(__name__)


def clear_primary_navigation_cache(instance: Model, **kwargs) -> None:
    """
    Clear primary navigation server-side cache and the front-end cache
    for two levels of pages site-wide.
    """
    if instance is None or not isinstance(instance, Page):
        return

    instance = instance.specific
    site = instance.get_site()

    if site is None or site.root_page is None:
        return

    if not utils.is_promotional_site(site):
        return

    if isinstance(instance, PromotionalSiteConfiguration):
        site_config = instance
    else:
        try:
            site_config = utils.get_promotional_site_configuration(site)
        except utils.PromotionalSiteConfigurationDoesNotExist:
            logger.exception(
                "Failed to get promotional site configuration for site_pk=%s.", site.pk
            )
            return

    # Clear navigation cache.
    primary_nav = PrimaryNavigation(site_config=site_config, site=site, cache=cache)

    try:
        primary_nav.clear_cache()
    except Exception:
        logger.exception(
            "Failed to clear primary navigation cache for a promotional site_pk=%s.",
            site.pk,
        )

    # Clear front-end cache
    purge_batch = PurgeBatch()
    purge_batch.add_page(site.root_page.specific)

    # Clear all direct children of the root page as well.
    # Exclude the page being published/unpublished as that is already purged separately.
    purge_batch.add_pages(
        site.root_page.specific.get_children().exclude(pk=instance.pk).live().specific()
    )
    try:
        purge_batch.purge()
    except Exception:
        logger.exception(
            "Failed to purge front-end cache for a promotional site_pk=%s.", site.pk
        )


page_published.connect(clear_primary_navigation_cache)
page_unpublished.connect(clear_primary_navigation_cache)
