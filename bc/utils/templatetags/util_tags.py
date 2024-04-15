from django import template
from django.conf import settings
from wagtail.coreutils import camelcase_to_underscore

from bc.utils.models import ImportantPages, SocialMediaSettings

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
    return settings.WAGTAILADMIN_BASE_URL


# Get directory base URL
@register.simple_tag(name="get_directory_url", takes_context=True)
def get_directory_url(context):
    request = context["request"]
    setting = ImportantPages.for_request(request)
    if setting:
        return setting.directory_url
