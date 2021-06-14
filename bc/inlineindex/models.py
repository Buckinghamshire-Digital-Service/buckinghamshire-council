import itertools

from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class InlineIndexMixin(object):
    """
    Mixin to define shared functionality between the index and the child pages.

    This could have been a base class for the other two page types as well. But, at the
    time of creation of this mixin, the pages have already been used widely and I don't
    want to go through the trouble messing with the model inheritance in the database.

    Most of the methods here only raise the `NotImplementedError` to signal a missing
    implementation in the derived classes. This is the case for the methods that should
    be present in the derived classes, but that differs for index pages and child pages.
    In that sense, this mixin acts like an interface. Other than an interface, it also
    does define concrete implementations.

    """

    def draft_for_page_available(self):
        return self.has_unpublished_changes or not self.live

    def viewing_page_draft(self, request):
        return request.is_preview and self.draft_for_page_available()

    def get_index_page_and_children(self, include_draft_pages):
        raise NotImplementedError

    def get_prev_page(self, include_draft_pages):
        raise NotImplementedError

    def get_next_page(self, include_draft_pages):
        raise NotImplementedError

    def get_context(self, request):
        context = super().get_context(request)

        include_draft_pages = self.viewing_page_draft(request)

        context["index"] = self.get_index_page_and_children(include_draft_pages)
        context["next_page"] = self.get_next_page(include_draft_pages)
        context["prev_page"] = self.get_prev_page(include_draft_pages)

        return context

    @cached_property
    def index_title(self):
        raise NotImplementedError

    @cached_property
    def content_title(self):
        raise NotImplementedError

    def __str__(self):
        return self.content_title


class InlineIndexRelatedPage(RelatedPage):
    source_page = ParentalKey("InlineIndex", related_name="related_pages")


class InlineIndex(InlineIndexMixin, BasePage):
    """A page with an included table of contents, listing this page and its children.

    InlineIndex and InlineIndexChild can be used to build a "guide" to a service or
    topic. All of the pages are shown together in a flat hierarchy in the table of
    contents, with the index page shown as the first sibling. The "next" and "previous"
    buttons navigate through the guide.

    See e.g. https://www.gov.uk/attendance-allowance for the GDS pattern that this
    implements.
    """
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

    def get_index_page_and_children(self, include_draft_children=False):
        index_queryset = Page.objects.page(self).specific()

        children = self.get_children().specific()
        if not include_draft_children:
            children = children.live()

        return itertools.chain(index_queryset, children)

    def get_next_page(self, include_draft_children=False):
        """ In fact returns the first child, instead, as this page acts as the
        first item in the index.
        """
        children = self.get_children()
        if not include_draft_children:
            children = children.live()

        return children.specific().first()

    def get_prev_page(self, *args, **kwargs):
        """Always return None because the index does not have a previous page."""
        return None

    @cached_property
    def index_title(self):
        return self.title

    @cached_property
    def content_title(self):
        return self.subtitle


class InlineIndexChild(InlineIndexMixin, BasePage):
    template = InlineIndex.template

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

    def get_index_page_and_children(self, include_draft_children=False):
        return self.get_parent().specific.get_index_page_and_children(
            include_draft_children,
        )

    def get_next_page(self, include_draft_pages=False):
        """ Return the next sibling, if there is one. NB this is implemented
        differently on InlineIndex.
        """
        next_siblings = self.get_next_siblings()
        if not include_draft_pages:
            next_siblings = next_siblings.live()

        next_page = next_siblings.first()
        if next_page:
            return next_page.specific

    def get_prev_page(self, include_draft_pages=False):
        """ Return the previous sibling, or in the case of a first child, the
        parent. NB this method is not implemented on InlineIndex, so the
        template just gets None.
        """
        prev_siblings = self.get_prev_siblings()
        if not include_draft_pages:
            prev_siblings = prev_siblings.live()

        prev_page = prev_siblings.first() or self.get_parent()
        if prev_page:
            return prev_page.specific

    @cached_property
    def index_title(self):
        return self.get_parent().specific.index_title

    @cached_property
    def content_title(self):
        return self.title
