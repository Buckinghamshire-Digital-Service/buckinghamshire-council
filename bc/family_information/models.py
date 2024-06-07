from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.coreutils import resolve_model_string
from wagtail.models import Page
from wagtail.search import index

from ..news.models import NewsIndex
from ..standardpages.models import IndexPage
from ..utils.models import BasePage


class FISBannerFields(models.Model):
    banner_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        blank=True,
        on_delete=models.SET_NULL,
    )
    banner_title = models.TextField(blank=True)
    banner_description = models.TextField(blank=True)
    banner_link = models.URLField(blank=True)
    banner_link_text = models.CharField(max_length=100, blank=True)

    search_fields = [
        index.SearchField("banner_title"),
        index.SearchField("banner_description"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
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

    def clean(self):
        super().clean()
        # either all are filled, or none are filled
        if (
            self.banner_image
            or self.banner_title
            or self.banner_description
            or self.banner_link
            or self.banner_link_text
        ) and not (
            self.banner_image
            and self.banner_title
            and self.banner_description
            and self.banner_link
            and self.banner_link_text
        ):
            raise ValidationError(
                {
                    "banner_image": "Either all or none of the banner fields must be filled"
                }
            )

    def has_banner_fields(self):
        return (
            self.banner_image
            and self.banner_title
            and self.banner_description
            and self.banner_link
        )


class SubsiteHomePage(FISBannerFields, BasePage):
    template = "patterns/pages/home/home_page--fis.html"

    parent_page_types = ["wagtailcore.Page"]

    is_pensions_site = models.BooleanField(default=False)

    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    description = models.TextField(blank=True)
    search_placeholder = models.CharField(max_length=100, blank=True)

    heading = models.CharField(
        blank=True, default="Get information, advice and guidance", max_length=255
    )

    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_prompt_text = models.TextField(
        blank=True, help_text="Text to prompt user to search"
    )

    search_fields = (
        BasePage.search_fields
        + FISBannerFields.search_fields
        + [index.SearchField("description")]
    )

    content_panels = (
        BasePage.content_panels
        + [
            FieldPanel("is_pensions_site"),
            MultiFieldPanel(
                [
                    FieldPanel("hero_image"),
                    FieldPanel("description"),
                    FieldPanel("search_placeholder"),
                ],
                heading="Hero",
            ),
            FieldPanel("heading"),
        ]
        + FISBannerFields.content_panels
        + [FieldPanel("search_prompt_text"), FieldPanel("call_to_action")]
    )

    @cached_property
    def child_pages(self):
        """Get child pages for the homepage listing.

        Returns a queryset of this page's live, public children, of the following page types
        - CategoryPage, CategoryTypeOnePage, CategoryTypeTwoPage, IndexPage, NewsIndex
        ordered by Wagtail explorer custom sort (ie. path).
        """
        return (
            Page.objects.child_of(self)
            .filter(
                content_type__in=ContentType.objects.get_for_models(
                    CategoryPage,
                    CategoryTypeOnePage,
                    CategoryTypeTwoPage,
                    IndexPage,
                    NewsIndex,
                ).values()
            )
            .filter(show_in_menus=True)
            .live()
            .public()
            .specific()
            .order_by("path")
        )


class BaseCategoryPage(FISBannerFields, BasePage):
    parent_page_types = ["SubsiteHomePage"]

    content_panels = BasePage.content_panels + FISBannerFields.content_panels
    search_fields = BasePage.search_fields + FISBannerFields.search_fields

    class Meta:
        abstract = True

    @classmethod
    def allowed_subpage_models(cls):
        return super().allowed_subpage_models() + [
            resolve_model_string("standardpages.IndexPage")
        ]

    @cached_property
    def child_pages(self):
        return self.get_children().live().public().specific().order_by("path")


class CategoryTypeOnePage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-cat1.html"
    is_creatable = False


class CategoryTypeTwoPage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-cat2.html"
    is_creatable = False


class CategoryPage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-cat.html"
    display_banner_at_top = models.BooleanField(default=False)

    content_panels = (
        BasePage.content_panels
        + [FieldPanel("display_banner_at_top")]
        + FISBannerFields.content_panels
    )

    def get_template(self, request, *args, **kwargs):
        if self.display_banner_at_top:
            return "patterns/pages/standardpages/index_page--fis-cat2.html"
        else:
            return "patterns/pages/standardpages/index_page--fis-cat1.html"


class School(index.Indexed, models.Model):
    class HubEmail(models.TextChoices):
        SENSCB = "sencsb@buckinghamshire.gov.uk", "sencsb@buckinghamshire.gov.uk"
        SENWYC = "senwyc@buckinghamshire.gov.uk", "senwyc@buckinghamshire.gov.uk"
        SENAYLESBURY = "Senaylesbury@buckinghamshire.gov.uk", "Senaylesbury@buckinghamshire.gov.uk"

    name = models.TextField()
    hub_email = models.CharField(choices=HubEmail.choices, blank=True, )
    ehc_co = models.ForeignKey(
        "family_information.EHCCo",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="schools",
    )

    def clean(self) -> None:
        super().clean()
        if not (self.hub_email or self.ehc_co):
            raise ValidationError(
                {
                    "hub_email": "Either hub email or EHCCo should be filled",
                    "ehc_co": "Either hub email or EHCCo should be filled",
                }
            )

    search_fields = [
        index.SearchField("name"),
    ]

    def __str__(self):
        return self.name


class EHCCo(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField("name"),
    ]

    class Meta:
        verbose_name = "EHCCo"
        verbose_name_plural = "EHCCos"
