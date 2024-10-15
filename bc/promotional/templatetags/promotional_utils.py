from django import template

from wagtail.models import Site

from .. import utils

register = template.Library()


@register.simple_tag(
    takes_context=True,
)
def is_promotional_site(context) -> bool:
    request = context["request"]
    current_site = Site.find_for_request(request)

    return utils.is_promotional_site(current_site)
