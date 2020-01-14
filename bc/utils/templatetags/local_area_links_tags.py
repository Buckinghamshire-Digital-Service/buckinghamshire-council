from django import template

register = template.Library()


@register.inclusion_tag("patterns/molecules/area-links-list/area-links-list.html")
def local_area_links(page):

    try:
        for data in page.body.stream_data:
            if data["type"] == "local_area_links":
                return {
                    "show_intro": True,
                    "value": data["value"],
                }

    except AttributeError:
        # Return empty if page does not have body field
        pass

    return None
