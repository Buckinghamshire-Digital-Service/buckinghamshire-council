from logging import getLogger

from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

import phonenumbers

logger = getLogger(__name__)


class PhoneNumberBlock(blocks.CharBlock):
    def clean(self, value):
        value = super().clean(value)
        if not value:
            raise ValidationError("Please enter a valid phone number")

        try:
            phone_number = phonenumbers.parse(value, "GB")
        except phonenumbers.NumberParseException:
            raise ValidationError("Please enter a valid phone number")
        except Exception:
            logger.exception(
                "Unexpected exception happened when trying to parse a phone number"
            )
            raise ValidationError("Could not parse the phone number")

        if not phonenumbers.is_possible_number(phone_number):
            raise ValidationError("Please enter a valid phone number")

        return phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.E164
        )


class CardLinkStructValue(blocks.StructValue):
    def get_button_link_block(self):
        button_link = self.get("button_link")
        return button_link[0] if button_link else None

    # return an href-ready value for button_link
    def get_button_link(self):
        block = self.get_button_link_block()

        if not block:
            return None

        match block.block_type:
            case "internal_link" if block.value and block.value.live:
                return block.value.url
            case "external_link":
                return block.value
            case "email":
                return f"mailto:{block.value}"
            case "phone_number":
                try:
                    phone_number = phonenumbers.parse(block.value, "GB")

                except phonenumbers.NumberParseException:
                    logger.exception(
                        "Invalid phone number found when trying to parse a value "
                        "from the database"
                    )
                    return None
                except Exception:
                    logger.exception(
                        "Unexpected exception when trying to parse a phone number "
                        "from the database"
                    )
                    return None

                number = phonenumbers.format_number(
                    phone_number, phonenumbers.PhoneNumberFormat.RFC3966
                )
                return number
            case _:
                return None


class LinkCard(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    description = blocks.TextBlock(max_length=255)
    image = ImageChooserBlock()
    button_text = blocks.CharBlock(max_length=128)
    button_link = blocks.StreamBlock(
        [
            ("internal_link", blocks.PageChooserBlock()),
            ("external_link", blocks.URLBlock()),
            ("email", blocks.EmailBlock()),
            (
                "phone_number",
                PhoneNumberBlock(),
            ),
        ],
        required=True,
        max_num=1,
    )

    class Meta:
        value_class = CardLinkStructValue


class LinkCards(blocks.StructBlock):
    items = blocks.ListBlock(LinkCard, max_num=3)
    link_page = blocks.PageChooserBlock(required=False)
    link_text = blocks.CharBlock(max_length=64, required=False)

    class Meta:
        icon = "grip"
        template = "patterns/organisms/promotional-cards/promotional-cards.html"

    def clean(self, value):
        cleaned_data = super().clean(value)

        if cleaned_data.get("link_page") and not cleaned_data.get("link_text"):
            raise blocks.StructBlockValidationError(
                block_errors={
                    "link_text": ValidationError(
                        "Link text is required if a link page has been set."
                    )
                }
            )

        return cleaned_data

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
            button_url = item.get_button_link()

            # Skip cards without link
            if not button_url:
                continue

            items.append(
                {
                    "title": item["title"],
                    "description": item["description"],
                    "image": item["image"],
                    "link_url": button_url,
                    "link_text": item["button_text"],
                    "link_highlight": False,
                }
            )

        if items:
            items[-1].update({"link_highlight": True})

        return items
