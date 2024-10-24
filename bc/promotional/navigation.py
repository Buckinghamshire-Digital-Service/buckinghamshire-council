import logging
from typing import MutableSequence, Optional, Sequence, TypedDict
from urllib.parse import urlparse

from django.core.cache import BaseCache

from wagtail.models import Site

from .models import PromotionalSiteConfiguration
from .models.configuration import PrimaryNavigationItem as PrimaryNavigationItemBlock
from .models.configuration import (
    PrimaryNavigationSection as PrimaryNavigationSectionBlock,
)

logger = logging.getLogger(__name__)


class PrimaryNavigationSubItem(TypedDict):
    title: str
    current: bool
    url: str
    is_on_current_site: bool


class PrimaryNavigationItem(TypedDict):
    title: str
    current: bool

    # Top-level nav item may be a page.
    url: Optional[str]
    is_on_current_site: Optional[bool]
    items: Sequence[PrimaryNavigationSubItem]


class PrimaryNavigation:
    cache: Optional[BaseCache]
    cache_prefix: str
    site: Site
    site_config: PromotionalSiteConfiguration
    CACHE_VERSION: Optional[int] = 2

    def __init__(
        self,
        *,
        site_config: PromotionalSiteConfiguration,
        site: Site,
        cache: Optional[BaseCache],
        cache_prefix: str = "promotional_primary_navigation"
    ) -> None:
        self.cache = cache
        self.cache_prefix = cache_prefix
        self.site = site
        self.site_config = site_config

    def fetch_navigation_items(
        self, *, current_path: str
    ) -> Sequence[PrimaryNavigationItem]:
        if self.cache:
            nav = self.cache.get_or_set(
                self.cache_key(), self.build_navigation, version=self.CACHE_VERSION
            )
        else:
            nav = self.build_navigation()
        return self.populate_navigation(nav=nav, current_path=current_path)

    def cache_key(self) -> str:
        return ":".join((self.cache_prefix, str(self.site.pk)))

    def build_navigation(self) -> Sequence[PrimaryNavigationItem]:
        """
        Take the StreamField blocks and build a navigation structure
        that only uses primitive types so that we can for example
        put it in the cache and not have any complicated logic
        live in the navigation template.
        """
        nav: MutableSequence[PrimaryNavigationItem] = []

        for item in self.site_config.primary_navigation:
            if isinstance(item.block, PrimaryNavigationItemBlock):

                page = item.value["page"]
                if page is None or not page.live:
                    # Skip pages that are not live or not existent anymore.
                    continue

                page = page.specific

                nav.append(
                    PrimaryNavigationItem(
                        current=False,
                        is_on_current_site=page.get_site() == self.site,
                        url=page.get_url(current_site=self.site),
                        items=[],
                        title=item.value["title"] or page.title,
                    )
                )
            elif isinstance(item.block, PrimaryNavigationSectionBlock):
                subitems: MutableSequence[PrimaryNavigationSubItem] = []
                for subitem in item.value["items"]:
                    subpage = subitem["page"]
                    # NB We don't validate page view restrictions. Worst case scenario a link
                    # is inaccessible from the nav.
                    # Skip deleted pages and non-live pages.
                    if subpage is None or not subpage.live:
                        continue

                    subpage = subpage.specific
                    on_current_site = subpage.get_site() == self.site
                    subitems.append(
                        PrimaryNavigationSubItem(
                            current=False,
                            is_on_current_site=on_current_site,
                            title=subitem["title"] or subpage.title,
                            url=subpage.get_url(current_site=self.site),
                        )
                    )
                if subitems:
                    nav.append(
                        PrimaryNavigationItem(
                            url=None,
                            is_on_current_site=None,
                            current=False,
                            items=subitems,
                            title=item.value["title"] or subpage.title,
                        )
                    )
        return nav

    def populate_navigation(
        self, *, current_path: str, nav: Sequence[PrimaryNavigationItem]
    ) -> Sequence[PrimaryNavigationItem]:
        """
        Once we fetch the navigation from cache or wherever,
        we want to populate any dynamic runtime content such as the current page status.
        """
        populated_nav: MutableSequence[PrimaryNavigationItem] = []
        for item in nav:
            populated_subitems = []
            item_current = False
            for subitem in item["items"]:
                subitem_current = self.subitem_is_current(
                    item=subitem, current_path=current_path
                )
                if subitem_current:
                    item_current = True
                populated_subitems.append({**subitem, "current": subitem_current})
            if (
                item_current is False
                and item["url"] is not None
                and item["is_on_current_site"] is True
            ):
                item_current = self._url_is_current(
                    url=item["url"], current_path=current_path
                )
            populated_nav.append(
                {**item, "items": populated_subitems, "current": item_current}
            )
        return populated_nav

    def subitem_is_current(
        self, *, item: PrimaryNavigationSubItem, current_path: str
    ) -> bool:
        if not item["is_on_current_site"]:
            return False
        return self._url_is_current(url=item["url"], current_path=current_path)

    def _url_is_current(self, *, url: str, current_path: str) -> bool:
        # Root page will escape the following check.
        # NB this will only work if the homepage is actually on "/".
        if url == "/" and current_path != "/":
            return False

        # In case the page URL is absolute, we want to extract the path only.
        # Although, this should not happen as we are only dealing with pages
        # on the current site.
        parsed_item_url_path = urlparse(url).path
        return parsed_item_url_path is not None and current_path.startswith(
            parsed_item_url_path
        )

    def clear_cache(self) -> None:
        """
        Clear the navigation server-side cache.

        This is called from signal handlers that also deal with the front-end cache.
        """
        if self.cache is not None:
            logger.info("PrimaryNavigation cache cleared for site_pk=%s", self.site.pk)
            self.cache.delete(self.cache_key(), version=self.CACHE_VERSION)
        else:
            logger.warning(
                "PrimaryNavigation cache for site_pk=%s was not cleared because cache is not set",
                self.site.pk,
            )
