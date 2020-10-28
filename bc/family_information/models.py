from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from ..utils.models import BasePage


class FISBannerFields(models.Model):
    banner_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    banner_title = models.TextField()
    banner_description = models.TextField()
    banner_link = models.URLField()
    banner_link_text = models.CharField(max_length=100, blank=True)

    search_fields = [
        index.SearchField("banner_title"),
        index.SearchField("banner_description"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("banner_image"),
                FieldPanel("banner_title"),
                FieldPanel("banner_description"),
                FieldPanel("banner_link"),
                FieldPanel("banner_link_text"),
            ],
            heading="Banner",
        ),
    ]

    class Meta:
        abstract = True


class FamilyInformationHomePage(FISBannerFields, BasePage):
    template = "patterns/pages/home/home_page--fis.html"

    subpage_types = ["CategoryTypeOnePage", "CategoryTypeTwoPage"]

    max_count = 1

    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    description = models.TextField(blank=True)
    search_placeholder = models.CharField(max_length=100, blank=True)

    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = (
        BasePage.search_fields
        + FISBannerFields.search_fields
        + [index.SearchField("description")]
    )

    content_panels = (
        BasePage.content_panels
        + [
            MultiFieldPanel(
                [
                    ImageChooserPanel("hero_image"),
                    FieldPanel("description"),
                    FieldPanel("search_placeholder"),
                ],
                heading="Hero",
            ),
        ]
        + FISBannerFields.content_panels
        + [SnippetChooserPanel("call_to_action")]
    )

    @cached_property
    def category_pages(self):
        """Get category pages for the homepage listing.

        Returns a queryset of this page's live, public children of either of the two
        CategoryTypeX classes, ordered by Wagtail explorer custom sort (ie. path).
        """
        return (
            Page.objects.child_of(self)
            .filter(
                content_type__in=ContentType.objects.get_for_models(
                    CategoryTypeOnePage, CategoryTypeTwoPage
                ).values()
            )
            .filter(show_in_menus=True)
            .live()
            .public()
            .specific()
            .order_by("path")
        )


class BaseCategoryPage(FISBannerFields, BasePage):
    parent_page_types = ["FamilyInformationHomePage"]
    subpage_types = ["inlineindex.InlineIndex"]

    content_panels = BasePage.content_panels + FISBannerFields.content_panels
    search_fields = BasePage.search_fields + FISBannerFields.search_fields

    class Meta:
        abstract = True

    @cached_property
    def child_pages(self):
        return self.get_children().live().public().specific().order_by("path")


class CategoryTypeOnePage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-send.html"


class CategoryTypeTwoPage(BaseCategoryPage):
    template = "patterns/pages/family_information/category_type_2.html"
