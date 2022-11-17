from urllib.parse import unquote

from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.search import index

from bc.utils.blocks import StoryBlock, WasteWizardSnippetBlock
from bc.utils.models import BasePage, RelatedPage


class InformationPageRelatedPage(RelatedPage):
    source_page = ParentalKey("InformationPage", related_name="related_pages")


class BaseInformationPage(BasePage):
    display_contents = models.BooleanField(default=False)

    intro_text = models.TextField(blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("display_contents"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    CONTENT_PANEL_BLOCKTYPES = ["heading"]

    @cached_property
    def live_related_pages(self):
        if not hasattr(self, "related_pages"):
            return []
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]

    @cached_property
    def h2_blocks(self):
        return [
            block
            for block in self.body
            if block.block_type in BaseInformationPage.CONTENT_PANEL_BLOCKTYPES
        ]

    class Meta:
        abstract = True


class InformationPage(BaseInformationPage):
    template = "patterns/pages/standardpages/information_page.html"

    body = StreamField(StoryBlock(), use_json_field=True)


class StoryBlockWithWasteWizard(StoryBlock):
    waste_wizard = WasteWizardSnippetBlock()

    class Meta:
        block_counts = {"waste_wizard": {"max_num": 1}}


class WasteWizardPage(BaseInformationPage):
    template = "patterns/pages/standardpages/information_page.html"
    is_waste_wizard_page = True

    body = StreamField(StoryBlockWithWasteWizard(), use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("display_contents"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
    ]

    def rc_consent_required(self):
        return any([block.block_type == "waste_wizard" for block in self.body])

    def has_rc_consent(self, request):
        return self.rc_consent_required() and (
            "agree to rc" in unquote(request.COOKIES.get("client-cookie", ""))
        )


class IndexPage(BasePage):
    template = "patterns/pages/standardpages/index_page.html"

    parent_page_types = [
        "home.HomePage",
        "family_information.CategoryTypeOnePage",
        "family_information.CategoryTypeTwoPage",
        "IndexPage",
        "family_information.SubsiteHomePage",
    ]

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("introduction")]

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    @cached_property
    def child_pages(self):
        return self.get_children().live().public().specific().order_by("path")

    @property
    def ordinary_pages(self):
        return self.child_pages[3:]

    @property
    def featured_pages(self):
        """
        Used by homepage TOC to get top 3 for listing
        """
        return self.child_pages[:3]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["featured_pages"] = self.featured_pages
        context["ordinary_pages"] = self.ordinary_pages

        return context
