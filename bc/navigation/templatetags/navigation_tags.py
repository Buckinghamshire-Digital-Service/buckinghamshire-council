from django import template

from bc.navigation.models import NavigationSettings

register = template.Library()


# Footer nav snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/footernav.html", takes_context=True
)
def footernav(context):
    request = context["request"]
    nav_settings = NavigationSettings.for_request(request)
    return {
        "columns": nav_settings.footer_columns,
        "links": nav_settings.footer_links,
        "request": request,
    }
