from functools import partial


from wagtail.core import blocks
from wagtail.images import blocks as image_blocks

from bc.utils.blocks import ButtonBlock, ImageOrEmbedBlock


CampaignRichTextBlock = partial(
    blocks.RichTextBlock,
    features=["link", "bold", "italic", "ul", "ol"]
)


class MediaSubheadingParagraphBlock(blocks.StructBlock):
    image_or_embed = ImageOrEmbedBlock(
        form_classname="struct-block c-sf-block c-sf-block__content-inner"
    )
    subheading = blocks.CharBlock(
        max_length=250,
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
    )
    paragraph = CampaignRichTextBlock()

    class Meta:
        icon = "media"
        template = "patterns/molecules/campaigns/blocks/media-subheading-paragraph-block.html"


class SubheadingParagraphBlock(blocks.StructBlock):
    subheading = blocks.CharBlock(
        max_length=250,
        template="patterns/molecules/streamfield/blocks/subheading_block.html",
    )
    paragraph = CampaignRichTextBlock()

    class Meta:
        icon = "pilcrow"
        template = "patterns/molecules/campaigns/blocks/subheading-paragraph-block.html"


class ButtonBannerValue(blocks.StructValue):
    def link(self):
        button = self.get("button")
        if button:
            external_url = button.get("link_url")
            page = button.get("link_page")
            if external_url:
                return external_url
            elif page:
                return page.url

    def link_text(self):
        button = self.get("button")
        if button:
            return button.get("text")


class DirectoryBannerValue(ButtonBannerValue):
    def to_dict(self):
        return {
            "banner_image": self.get("image"),
            "banner_title": self.get("title"),
            "banner_description": self.get("description"),
            "banner_link": self.link(),
            "banner_link_text": self.link_text(),
        }


class DirectoryBannerBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock()
    title = blocks.TextBlock()
    description = blocks.TextBlock()
    button = ButtonBlock(
        form_classname="struct-block c-sf-block c-sf-block__content-inner"
    )

    class Meta:
        icon = "tag"
        value_class = DirectoryBannerValue
        template = "patterns/molecules/campaigns/blocks/directory-banner.html"


class FullWidthBanner(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=250)
    text = blocks.TextBlock()
    button = ButtonBlock(
        form_classname="struct-block c-sf-block c-sf-block__content-inner"
    )

    class Meta:
        icon = "arrow-right"
        value_class = ButtonBannerValue
        template = "patterns/molecules/campaigns/blocks/full-width-banner.html"


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        form_classname="full title",
        template="patterns/molecules/streamfield/blocks/heading_block.html",
    )

    content = blocks.StreamBlock(
        [
            ("media_with_subheading_and_paragraph", MediaSubheadingParagraphBlock()),
            ("subheading_and_paragraph", SubheadingParagraphBlock()),
            ("directory_banner", DirectoryBannerBlock()),
            ("full_width_banner", FullWidthBanner()),
        ]
    )

    class Meta:
        template = "patterns/molecules/campaigns/blocks/campaign-section.html"
