from wagtail.models import Site

from .models import PromotionalHomePage, PromotionalSiteConfiguration


def is_promotional_site(site: Site, /) -> bool:
    return isinstance(site.root_page.specific, PromotionalHomePage)


class PromotionalSiteConfigurationDoesNotExist(Exception):
    pass


def get_promotional_site_configuration(site: Site, /) -> PromotionalSiteConfiguration:
    try:
        return PromotionalSiteConfiguration.objects.in_site(site).live().get()
    except PromotionalSiteConfiguration.DoesNotExist as e:
        raise PromotionalSiteConfigurationDoesNotExist(
            "No PromotionalSiteConfiguration instance found in this site."
        ) from e
