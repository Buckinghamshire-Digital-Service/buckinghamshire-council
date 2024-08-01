import logging

from django.conf import settings

from wagtail.models import Site

from bc.family_information.utils import is_subsite
from bc.recruitment.utils import is_recruitment_site
from bc.utils.constants import (
    BASE_PAGE_TEMPLATE,
    BASE_PAGE_TEMPLATE_FAMILY_INFORMATION,
    BASE_PAGE_TEMPLATE_RECRUITMENT,
)

logger = logging.getLogger(__name__)


def global_vars(request):
    if site := Site.find_for_request(request):
        if is_subsite(site):
            base_page_template = BASE_PAGE_TEMPLATE_FAMILY_INFORMATION
        elif is_recruitment_site(site):
            base_page_template = BASE_PAGE_TEMPLATE_RECRUITMENT
        else:
            base_page_template = BASE_PAGE_TEMPLATE

        is_pensions_site = (
            base_page_template == BASE_PAGE_TEMPLATE_FAMILY_INFORMATION
        ) and site.root_page.specific.is_pensions_site
    else:
        logger.warning(
            "No site found for request - has the default site been unset or deleted?"
        )
        base_page_template = BASE_PAGE_TEMPLATE
        is_pensions_site = False

    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", None),
        "YANDEX_VERIFICATION_STRING": getattr(
            settings, "YANDEX_VERIFICATION_STRING", None
        ),
        "FATHOM_SITE_ID": getattr(settings, "FATHOM_SITE_ID", None),
        "base_page_template": base_page_template,
        "is_pensions_site": is_pensions_site,
        "COOKIE_DOMAIN": getattr(settings, "COOKIE_DOMAIN", None),
        "NONINDEXED_HOSTS": getattr(settings, "NONINDEXED_HOSTS", []),
        "GOOGLE_MAPS_V3_APIKEY": getattr(settings, "GOOGLE_MAPS_V3_APIKEY", ""),
    }
