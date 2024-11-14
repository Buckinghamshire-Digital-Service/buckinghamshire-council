from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkCard(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    description = blocks.TextBlock(max_length=255)
    image = ImageChooserBlock()
    link_page = blocks.PageChooserBlock(
        required=False,
        help_text="Please choose an internal page or specify the URL, not both at the same time",
    )
    link_url = blocks.URLBlock(
        required=False,
        label="Link URL",
        help_text="Please specify the URL or an internal page, not both at the same time",
    )
    link_text = blocks.CharBlock(max_length=128)

    def clean(self, value) -> None:
        result = super().clean(value)
        errors = {}
        if value["link_page"] is not None and value["link_url"]:
            errors["link_page"] = ValidationError(
                "Page cannot be specified at the same time as the URL"
            )
            errors["link_url"] = ValidationError(
                "URL cannot be specified at the same time as the page"
            )
        elif value["link_page"] is None and not value["link_url"]:
            msg = (
                "Page and URL fields cannot be both empty at the same time. "
                "Please specify value for one of those fields"
            )
            for key in ("link_page", "link_url"):
                errors[key] = ValidationError(msg)
        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)
        return result


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
            url = item["link_url"]

            if url:
                link_url = url
            elif page is not None and page.live:
                link_url = page.get_url(request=request)
            # Skip cards for deleted pages
            else:
                continue

            items.append(
                {
                    "title": item["title"],
                    "description": item["description"],
                    "image": item["image"],
                    "link_url": link_url,
                    "link_text": item["link_text"],
                    "link_highlight": False,
                }
            )
        items[-1]["link_highlight"] = True
        return items
