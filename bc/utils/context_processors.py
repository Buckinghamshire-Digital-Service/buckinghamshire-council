from django.conf import settings

from wagtail.core.models import Site

from bc.family_information.utils import is_family_information_site
from bc.recruitment.utils import is_recruitment_site
from bc.utils.constants import (
    BASE_PAGE_TEMPLATE,
    BASE_PAGE_TEMPLATE_FAMILY_INFORMATION,
    BASE_PAGE_TEMPLATE_RECRUITMENT,
)
from bc.utils.models import ImportantPages


def global_vars(request):
    site = Site.find_for_request(request)
    if is_family_information_site(site):
        base_page_template = BASE_PAGE_TEMPLATE_FAMILY_INFORMATION
    elif is_recruitment_site(site):
        base_page_template = BASE_PAGE_TEMPLATE_RECRUITMENT
    else:
        base_page_template = BASE_PAGE_TEMPLATE

    return {
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", None),
        "YANDEX_VERIFICATION_STRING": getattr(
            settings, "YANDEX_VERIFICATION_STRING", None
        ),
        "FATHOM_SITE_ID": getattr(settings, "FATHOM_SITE_ID", None),
        "base_page_template": base_page_template,
        "COOKIE_DOMAIN": getattr(settings, "COOKIE_DOMAIN", None),
        "NONINDEXED_HOSTS": getattr(settings, "NONINDEXED_HOSTS", []),
        "CONTACT_US_PAGE": ImportantPages.for_request(request).contact_us_page,
    }
