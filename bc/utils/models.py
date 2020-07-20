from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from bc.utils.cache import get_default_cache_control_decorator
from bc.utils.constants import RICH_TEXT_FEATURES

from .validators import validate_linkedin_domain, validate_youtube_domain


class LinkFields(models.Model):
    """
    Adds fields for internal and external links with some methods to simplify the rendering:

    <a href="{{ obj.get_link_url }}">{{ obj.get_link_text }}</a>
    """

    link_page = models.ForeignKey(
        "wagtailcore.Page", blank=True, null=True, on_delete=models.SET_NULL
    )
    link_url = models.URLField(blank=True)
    link_text = models.CharField(blank=True, max_length=255)

    class Meta:
        abstract = True

    def clean(self):
        if not self.link_page and not self.link_url:
            raise ValidationError(
                {
                    "link_url": ValidationError(
                        "You must specify link page or link url."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url."
                    ),
                }
            )

        if self.link_page and self.link_url:
            raise ValidationError(
                {
                    "link_url": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                }
            )

        if not self.link_page and not self.link_text:
            raise ValidationError(
                {
                    "link_text": ValidationError(
                        "You must specify link text, if you use the link url field."
                    )
                }
            )

    def get_link_text(self):
        if self.link_text:
            return self.link_text

        if self.link_page:
            return self.link_page.title

        return ""

    def get_link_url(self):
        if self.link_page:
            return self.link_page.get_url

        return self.link_url

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel("link_page"),
                FieldPanel("link_url"),
                FieldPanel("link_text"),
            ],
            "Link",
        )
    ]


# Related pages
class RelatedPage(Orderable, models.Model):
    page = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        abstract = True
        ordering = ["sort_order"]

    panels = [PageChooserPanel("page")]


# Generic social fields abstract class to add social image/text to any new content type easily.
class SocialFields(models.Model):
    social_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    social_text = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel(
            [ImageChooserPanel("social_image"), FieldPanel("social_text")],
            "Social networks",
        )
    ]


# Generic listing fields abstract class to add listing image/text to any new content type easily.
class ListingFields(models.Model):
    listing_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose the image you wish to be displayed when this page appears in listings",
    )
    listing_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Override the page title used when this page appears in listings",
    )
    listing_summary = models.CharField(
        max_length=255,
        blank=True,
        help_text="The text summary used when this page appears in listings. It's also used as "
        "the description for search engines if the 'Search description' field above is not defined.",
    )

    class Meta:
        abstract = True

    promote_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("listing_image"),
                FieldPanel("listing_title"),
                FieldPanel("listing_summary"),
            ],
            "Listing information",
        )
    ]


@register_snippet
class CallToActionSnippet(models.Model):
    title = models.CharField(max_length=255)
    summary = RichTextField(blank=True, max_length=255, features=RICH_TEXT_FEATURES)
    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    link = StreamField(
        blocks.StreamBlock(
            [
                (
                    "external_link",
                    blocks.StructBlock(
                        [("url", blocks.URLBlock()), ("title", blocks.CharBlock())],
                        icon="link",
                    ),
                ),
                (
                    "internal_link",
                    blocks.StructBlock(
                        [
                            ("page", blocks.PageChooserBlock()),
                            ("title", blocks.CharBlock(required=False)),
                        ],
                        icon="link",
                    ),
                ),
            ],
            required=True,
        ),
        blank=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("summary"),
        ImageChooserPanel("image"),
        StreamFieldPanel("link"),
    ]

    def __str__(self):
        return self.title


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter_handle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your Twitter username without the @, e.g. katyperry",
    )
    facebook_app_id = models.CharField(
        max_length=255, blank=True, help_text="Your Facebook app ID."
    )
    youtube_channel_url = models.URLField(
        blank=True,
        help_text="Your YouTube channel URL.",
        validators=[validate_youtube_domain],
    )
    instagram_username = models.CharField(
        max_length=255, blank=True, help_text="Your Instagram username."
    )
    linkedin_organisation_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your LinkedIn organisation page URL.",
        validators=[validate_linkedin_domain],
    )
    default_sharing_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default sharing text to use if social text has not been set on a page.",
    )
    site_name = models.CharField(
        max_length=255,
        blank=True,
        default="Buckinghamshire Council",
        help_text="Site name, used by Open Graph.",
    )

    def has_any_setting(self):
        return any(
            [
                self.twitter_handle,
                self.facebook_app_id,
                self.youtube_channel_url,
                self.instagram_username,
                self.linkedin_organisation_url,
            ]
        )


@register_setting
class SystemMessagesSettings(BaseSetting):
    class Meta:
        verbose_name = "system messages"

    title_404 = models.CharField("Title", max_length=255, default="Page not found")
    body_404 = RichTextField(
        "Text",
        default="<p>You may be trying to find a page that doesn&rsquo;t exist or has been moved.</p>",
        features=RICH_TEXT_FEATURES,
    )

    panels = [
        MultiFieldPanel([FieldPanel("title_404"), FieldPanel("body_404")], "404 page")
    ]


@register_setting
class SiteBannerSettings(BaseSetting):
    class Meta:
        verbose_name = "Site banner"

    show_banner = models.BooleanField(
        default=False,
        help_text="When set to True, the banner will be displayed on all pages of "
        + "the site except for homepage. For homepage, please use the alert fields on homepage.",
    )
    label = models.CharField("Alert label", max_length=255)
    body = RichTextField("Text", features=RICH_TEXT_FEATURES)

    panels = [
        MultiFieldPanel(
            [FieldPanel("show_banner"), FieldPanel("label"), FieldPanel("body")],
            "Banner",
        )
    ]


# Apply default cache headers on this page model's serve method.
@method_decorator(get_default_cache_control_decorator(), name="serve")
class BasePage(SocialFields, ListingFields, Page):
    show_in_menus_default = True
    redirect_to = models.URLField(
        blank=True,
        verbose_name="Redirect to external URL",
        help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
    )
    show_live_chat_client = models.BooleanField(
        default=False, help_text="Show live chat support client on this page"
    )

    class Meta:
        abstract = True

    promote_panels = (
        # extend Page.promote_panels
        [
            MultiFieldPanel(
                [
                    FieldPanel("slug"),
                    FieldPanel("seo_title"),
                    FieldPanel("show_in_menus"),
                    FieldPanel("search_description"),
                    FieldPanel("redirect_to"),
                ],
                "Common page configuration",
            )
        ]
        + SocialFields.promote_panels
        + ListingFields.promote_panels
        + [MultiFieldPanel([FieldPanel("show_live_chat_client")], "Page features")]
    )

    def serve(self, request, *args, **kwargs):
        if self.redirect_to and not getattr(request, "is_preview", False):
            return HttpResponseRedirect(self.redirect_to)

        return super().serve(request, *args, **kwargs)


BasePage._meta.get_field("seo_title").verbose_name = "Title tag"
BasePage._meta.get_field("search_description").verbose_name = "Meta description"


@register_setting
class ImportantPages(BaseSetting):
    contact_us_page = models.ForeignKey(
        "wagtailcore.Page", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    cookie_information_page = models.ForeignKey(
        "wagtailcore.Page", null=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        PageChooserPanel("contact_us_page"),
        PageChooserPanel("cookie_information_page"),
    ]
