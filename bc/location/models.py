from django.db import models
from django.db.models.expressions import Case, When
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    RichTextFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.rich_text import expand_db_html

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

    def map_markers(self):
        return [page.map_info for page in self.child_pages]


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

    map_location = models.TextField(blank=True)
    latlng = models.CharField(max_length=250, blank=True)
    map_info_text = RichTextField(
        blank=False,
        null=True,
        help_text="Content to display in popup window above the map",
    )
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

    body = StreamField(StoryBlock(), use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("image"),
        MultiFieldPanel(
            [
                GeoPanel("latlng", address_field="map_location", hide_latlng=True),
                FieldPanel("map_location"),
                RichTextFieldPanel("map_info_text"),
            ],
            "Map",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("street_address_1"), FieldPanel("street_address_2")]
                ),
                FieldRowPanel([FieldPanel("city"), FieldPanel("postcode")]),
            ],
            "Address",
        ),
        FieldRowPanel(
            [FieldPanel("telephone"), FieldPanel("email_address")], "Contact info"
        ),
        FieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.latlng)

    @property
    def map_info(self):
        return {
            "lat": self.point["y"] if self.point else "",
            "lng": self.point["x"] if self.point else "",
            "map_info_text": expand_db_html(self.map_info_text),
            "title": self.title,
            "url": self.url,
        }

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
