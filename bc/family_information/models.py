from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.coreutils import resolve_model_string
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from ..news.models import NewsIndex
from ..standardpages.models import IndexPage
from ..utils.blocks import DirectorySearchBlock
from ..utils.models import BasePage, PageTopTask
from .blocks import CardsBlock, ThreeCardRowBlock, TwoCardRowBlock


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


class SubsiteHomePageTopTask(PageTopTask):
    source = ParentalKey("family_information.SubsiteHomePage", related_name="top_tasks")


class SubsiteHomePage(FISBannerFields, BasePage):
    template = "patterns/pages/home/home_page--fis.html"

    parent_page_types = ["wagtailcore.Page"]

    is_pensions_site = models.BooleanField(default=False)

    # Hero
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    description = models.TextField(blank=True)
    search_placeholder = models.CharField(max_length=100, blank=True)

    # Top tasks
    top_tasks_heading = models.CharField(
        blank=True, default="What do you want to do?", max_length=255
    )

    # Highlighted cards
    highlighted_cards = StreamField(
        [
            ("two_card_row", TwoCardRowBlock()),
            ("three_card_row", ThreeCardRowBlock()),
        ],
        blank=True,
    )

    heading = models.CharField(
        blank=True, default="Get information, advice and guidance", max_length=255
    )

    directory_search = StreamField(
        [("directory_search", DirectorySearchBlock())], blank=True, max_num=1
    )

    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Footer
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
            MultiFieldPanel(
                [
                    FieldPanel("top_tasks_heading", heading="Heading"),
                    InlinePanel("top_tasks", label="Tasks"),
                ],
                heading="Top tasks",
            ),
            FieldPanel("heading"),
            FieldPanel("highlighted_cards"),
            FieldPanel("directory_search"),
        ]
        + FISBannerFields.content_panels
        + [FieldPanel("search_prompt_text"), FieldPanel("call_to_action")]
    )

    @cached_property
    def other_child_pages(self):
        """Get child pages for the homepage listing excluding children that are already
        in the highlighted_cards field.

        Returns a queryset of this page's live, public children, of the following page types
        - CategoryPage, CategoryTypeOnePage, CategoryTypeTwoPage, IndexPage, NewsIndex
        ordered by Wagtail explorer custom sort (ie. path).
        """
        highlighted_card_ids = [
            card.value.id for row in self.highlighted_cards for card in row.value
        ]
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
            .exclude(id__in=highlighted_card_ids)
            .live()
            .public()
            .specific()
            .order_by("path")
        )


class CategoryTypeOnePageTopTask(PageTopTask):
    source = ParentalKey(
        "family_information.CategoryTypeOnePage", related_name="top_tasks"
    )


class CategoryTypeTwoPageTopTask(PageTopTask):
    source = ParentalKey(
        "family_information.CategoryTypeTwoPage", related_name="top_tasks"
    )


class CategoryPageTopTask(PageTopTask):
    source = ParentalKey("family_information.CategoryPage", related_name="top_tasks")


class BaseCategoryPage(FISBannerFields, BasePage):
    parent_page_types = ["SubsiteHomePage"]

    # Top tasks
    top_tasks_heading = models.CharField(
        default="What do you want to do?", max_length=255
    )

    display_featured_images = models.BooleanField(default=False)

    # Content
    body = StreamField(
        [
            (
                "heading",
                blocks.CharBlock(
                    icon="title",
                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                ),
            ),
            ("cards", CardsBlock()),
        ],
        blank=True,
    )

    # Other child pages
    other_pages_heading = models.CharField(default="Others", max_length=255, blank=True)

    directory_search = StreamField(
        [
            (
                "directory_search",
                DirectorySearchBlock(
                    template="patterns/organisms/search-widget/search-widget.html"
                ),
            )
        ],
        blank=True,
        max_num=1,
    )

    content_panels = [
        FieldPanel("display_featured_images"),
        MultiFieldPanel(
            [
                FieldPanel("top_tasks_heading", heading="Heading"),
                InlinePanel("top_tasks", label="Tasks"),
            ],
            heading="Top tasks",
        ),
        FieldPanel(
            "body",
            help_text=(
                "This replaces the full list of child pages. Any child pages not "
                "listed in this field will be displayed under the 'Other pages' "
                "section."
            ),
        ),
        FieldPanel(
            "other_pages_heading",
            help_text=(
                "Any child pages not added to the Body field will be displayed "
                "below this heading. (If the Body field is blank, this heading "
                " isn't displayed.)"
            ),
        ),
        FieldPanel("directory_search"),
    ] + FISBannerFields.content_panels

    search_fields = BasePage.search_fields + FISBannerFields.search_fields

    class Meta:
        abstract = True

    @classmethod
    def allowed_subpage_models(cls):
        return super().allowed_subpage_models() + [
            resolve_model_string("standardpages.IndexPage")
        ]

    @cached_property
    def has_featured_pages(self):
        return any(row.block_type == "cards" for row in self.body)

    @cached_property
    def other_child_pages(self):
        """Get child pages for the current category page, excluding children that are
        already in the body field.
        """
        selected_card_ids = [
            card.value.id
            for row in self.body
            for card in row.value
            if row.block_type == "cards"
        ]
        return (
            self.get_children()
            .exclude(id__in=selected_card_ids)
            .live()
            .public()
            .specific()
            .order_by("path")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Get a list of all blocks that are below a heading block.
        context["blocks_under_headings"] = []
        has_heading = False
        for item in self.body:
            if item.block_type == "heading":
                has_heading = True
            elif has_heading:
                context["blocks_under_headings"].append(item.value)

        # Show the other_pages_heading field?
        context["show_other_pages_heading"] = (
            self.other_pages_heading and self.body and self.other_child_pages
        )

        return context


class CategoryTypeOnePage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-cat1.html"
    is_creatable = False


class CategoryTypeTwoPage(BaseCategoryPage):
    template = "patterns/pages/standardpages/index_page--fis-cat2.html"
    is_creatable = False


class CategoryPage(BaseCategoryPage):
    display_banner_at_top = models.BooleanField(default=False)

    content_panels = (
        BasePage.content_panels
        + [
            FieldPanel("display_banner_at_top"),
        ]
        + BaseCategoryPage.content_panels
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
        SENAYLESBURY = (
            "Senaylesbury@buckinghamshire.gov.uk",
            "Senaylesbury@buckinghamshire.gov.uk",
        )

    name = models.TextField()
    hub_email = models.CharField(
        choices=HubEmail.choices,
        blank=True,
    )
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
        index.AutocompleteField("name"),
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
