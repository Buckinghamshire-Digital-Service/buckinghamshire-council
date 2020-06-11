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
    "patterns/molecules/navigation/footerlinks.html", takes_context=True
)
def footerlinks(context):
    request = context["request"]
    return {
        "footerlinks": NavigationSettings.for_request(request).footer_links,
        "request": request,
    }
