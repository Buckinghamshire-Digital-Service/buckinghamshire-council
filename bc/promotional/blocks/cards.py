from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkCard(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    description = blocks.TextBlock(max_length=255)
    image = ImageChooserBlock()
    link_page = blocks.PageChooserBlock()
    link_text = blocks.CharBlock(max_length=128)


class LinkCards(blocks.StructBlock):
    items = blocks.ListBlock(LinkCard, max_num=3)
    link_page = blocks.PageChooserBlock(required=False)
    link_text = blocks.CharBlock(max_length=64, required=False)

    class Meta:
        icon = "grip"
        template = "patterns/organisms/promotional-cards/promotional-cards.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        request = context.get("request")

        context["items"] = self.get_items_context(value["items"], request=request)

        link_page = value["link_page"]
        if link_page is not None and link_page.live:
            context["link_url"] = link_page.get_url(request=request)
            context["link_text"] = value["link_text"]
        return context

    def get_items_context(self, items_value, *, request):
        items = []
        for item in items_value:
            page = item["link_page"]
            if page is None or not page.live:
                continue
            items.append(
                {
                    "title": item["title"],
                    "description": item["description"],
                    "image": item["image"],
                    "link_url": page.get_url(request=request),
                    "link_text": item["link_text"],
                    "link_highlight": False,
                }
            )
        items[-1]["link_highlight"] = True
        return items
