from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


def draft_for_page_available(page):
    return page.has_unpublished_changes or not page.live


def viewing_page_draft(page, request):
    return draft_for_page_available(page) and request.is_preview


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

    def get_index(self, include_draft_children=False):
        index_queryset = Page.objects.page(self)

        children = self.get_children().specific()
        if not include_draft_children:
            children = children.live()

        return index_queryset.union(children)

    def get_next_page(self, include_draft_children=False):
        """ In fact returns the first child, instead, as this page acts as the
        first item in the index.
        """
        children = self.get_children()
        if not include_draft_children:
            children = children.live()

        first_child = children.first()

        if first_child:
            return first_child.specific

    def get_context(self, request):
        context = super().get_context(request)

        include_draft_children = viewing_page_draft(self, request)

        context["index"] = self.get_index(include_draft_children)
        context["next_page"] = self.get_next_page(include_draft_children)

        return context


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

    def get_index(self, include_draft_children=False):
        return self.get_parent().specific.get_index(include_draft_children)

    def get_next_page(self, include_draft_pages=False):
        """ Return the next sibling, if there is one. NB this is implemented
        differently on InlineIndex.
        """
        next_siblings = self.get_next_siblings()
        if not include_draft_pages:
            next_siblings = next_siblings.live()

        next_sibling = next_siblings.first()
        if next_sibling:
            return next_sibling.specific

    def get_prev_page(self):
        """ Return the previous sibling, or in the case of a first child, the
        parent. NB this method is not implemented on InlineIndex, so the
        template just gets None.
        """
        prev_sibling = self.get_prev_sibling() or self.get_parent()

        if prev_sibling:
            return prev_sibling.specific

    def get_context(self, request):
        context = super().get_context(request)

        include_draft_pages = viewing_page_draft(self, request)

        context["index"] = self.get_index(include_draft_pages)
        context["next_page"] = self.get_next_page(include_draft_pages)
        context["prev_page"] = self.get_prev_page()
        return context

    def get_template(self, request):
        return InlineIndex().get_template(request)
