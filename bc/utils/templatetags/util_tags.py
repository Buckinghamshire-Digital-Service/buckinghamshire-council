from django import template
from django.conf import settings

from wagtail.core.utils import camelcase_to_underscore

from bc.utils.models import SocialMediaSettings

register = template.Library()


# Social text
@register.filter(name="social_text")
def social_text(page, site):
    try:
        if page.social_text:
            return page.social_text
    except AttributeError:
        pass

    return SocialMediaSettings.for_site(site).default_sharing_text


# Get widget type of a field
@register.filter(name="widget_type")
def widget_type(bound_field):
    return camelcase_to_underscore(bound_field.field.widget.__class__.__name__)


# Get type of field
@register.filter(name="field_type")
def field_type(bound_field):
    return camelcase_to_underscore(bound_field.field.__class__.__name__)


# Join lists, but not strings
@register.filter(name="join_list")
def join_list(value):
    if isinstance(value, list):
        return (", ").join(value)

    return value


# Get default site
@register.simple_tag(name="get_default_site")
def get_default_site():
    return settings.BASE_URL


# Get FIS directory base URL
@register.simple_tag(name="get_fis_directory")
def get_fis_directory():
    return settings.FIS_DIRECTORY_BASE_URL
