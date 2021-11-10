from django.db import models
from django.db.models.expressions import Case, When
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    RichTextFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailgeowidget.edit_handlers import GeoPanel
from wagtailgeowidget.helpers import geosgeometry_str_to_struct

from bc.area_finder.utils import validate_postcode
from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class LocationIndexPage(BasePage):
    template = "patterns/pages/location/location_index_page.html"
    subpage_types = ["location.LocationPage"]

    body = RichTextField()

    content_panels = BasePage.content_panels + [RichTextFieldPanel("body")]

    @cached_property
    def child_pages(self):
        pages = (
            LocationPage.objects.child_of(self)
            .live()
            .public()
            .annotate(
                display_title=Case(
                    When(listing_title="", then="title"), default="listing_title"
                )
            )
            .order_by("display_title")
        )

        return pages


class LocationPageRelatedPage(RelatedPage):
    source_page = ParentalKey("LocationPage", related_name="related_pages")


class LocationPage(BasePage):
    template = "patterns/pages/location/location_page.html"

    image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
    )

    map_location = models.CharField(max_length=250, blank=True)
    street_address_1 = models.CharField(blank=True, max_length=255)
    street_address_2 = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    postcode = models.CharField(
        blank=True, max_length=255, validators=[validate_postcode]
    )

    telephone = models.CharField(
        blank=True,
        max_length=16,
        help_text="This will be used for a tel: anchor link in the page",
    )
    email_address = models.EmailField(blank=True)

    body = StreamField(StoryBlock())

    content_panels = BasePage.content_panels + [
        ImageChooserPanel("image"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("street_address_1"), FieldPanel("street_address_2")]
                ),
                FieldRowPanel([FieldPanel("city"), FieldPanel("postcode")]),
                GeoPanel("map_location"),
            ],
            "Address",
        ),
        FieldRowPanel(
            [FieldPanel("telephone"), FieldPanel("email_address")], "Contact info"
        ),
        StreamFieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.map_location)

    @property
    def lat(self):
        return self.point["y"] if self.point else None

    @property
    def lng(self):
        return self.point["x"] if self.point else None

    @cached_property
    def address(self):
        return {
            "street_address_1": self.street_address_1,
            "street_address_2": self.street_address_2,
            "city": self.city,
            "postcode": self.postcode,
        }

    @cached_property
    def contact(self):
        return {
            "email_address": self.email_address,
            "telephone": self.telephone,
        }

    parent_page_types = ["location.LocationIndexPage"]

    @cached_property
    def live_related_pages(self):
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]
