from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class InlineIndexRelatedPage(RelatedPage):
    source_page = ParentalKey("InlineIndex", related_name="related_pages")


class InlineIndex(BasePage):
    template = "patterns/pages/inlineindex/inline_index_page.html"

    subtitle = models.CharField(
        max_length=255,
        help_text="Title that appears on the index. (e.g. Introduction)",
        default="Introduction",
    )

    body = StreamField(StoryBlock())

    is_inline_index = True
    is_inline_index_child = False

    subpage_types = [
        "inlineindex.InlineIndexChild",
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    @cached_property
    def live_related_pages(self):
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]

    def get_index(self):
        index_queryset = Page.objects.page(self)
        index_queryset = index_queryset.union(self.get_children().specific())
        return index_queryset

    def get_next_page(self):
        """ In fact returns the first child, instead, as this page acts as the
        first item in the index.
        """
        first_child = self.get_children().first()

        if first_child:
            return first_child.specific


class InlineIndexChild(BasePage):

    body = StreamField(StoryBlock())

    is_inline_index = False
    is_inline_index_child = True

    parent_page_types = [
        "inlineindex.InlineIndex",
    ]

    subpage_types = [
        "standardpages.InformationPage",
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel("body"),
    ]

    @cached_property
    def live_related_pages(self):
        return self.get_parent().specific.live_related_pages

    def get_index(self):
        return self.get_parent().specific.get_index()

    def get_next_page(self):
        """ Return the next sibling, if there is one. NB this is implemented
        differently on InlineIndex.
        """
        next_sibling = self.get_next_sibling()

        if next_sibling:
            return next_sibling.specific

    def get_template(self, request):
        return InlineIndex().get_template(request)

    def get_prev_page(self):
        """ Return the previous sibling, or in the case of a first child, the
        parent. NB this method is not implemented on InlineIndex, so the
        template just gets None.
        """
        prev_sibling = self.get_prev_sibling() or self.get_parent()

        if prev_sibling:
            return prev_sibling.specific
