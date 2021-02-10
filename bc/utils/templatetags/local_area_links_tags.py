from django import template

register = template.Library()


@register.inclusion_tag("patterns/molecules/area-links-list/area-links-list.html")
def local_area_links(page):

    try:
        for block in page.body:
            if block.block_type == "local_area_links":
                return {
                    "show_intro": True,
                    "value": block.value,
                }

    except AttributeError:
        # Return empty if page does not have body field
        pass

    return None
