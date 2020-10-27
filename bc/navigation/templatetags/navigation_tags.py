from django import template

from bc.navigation.models import NavigationSettings

register = template.Library()


# Sidebar snippets
@register.inclusion_tag(
    "patterns/molecules/navigation/sidebar.html", takes_context=True
)
def sidebar(context):
    return {
        "children": context["page"].get_children().live().public().in_menu(),
        "request": context["request"],
    }


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
