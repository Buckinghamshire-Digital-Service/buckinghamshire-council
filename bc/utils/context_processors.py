from django.conf import settings

from wagtail.core.models import Site

from bc.recruitment.utils import is_recruitment_site
from bc.utils.constants import BASE_PAGE_TEMPLATE, BASE_PAGE_TEMPLATE_RECRUITMENT


def global_vars(request):
    site = Site.find_for_request(request)
    if is_recruitment_site(site):
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
    }
