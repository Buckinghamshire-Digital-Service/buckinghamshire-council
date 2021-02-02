from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index

from bc.utils.models import BasePage

from .blocks import LongformStoryBlock


class LongformPage(BasePage):
    template = "patterns/pages/longform/longform_page.html"
    subpage_types = ["LongformChapterPage"]

    class Meta:
        verbose_name = "Long-form content page"

    is_chapter_page = False

    last_updated = models.DateField()
    version_number = models.CharField(blank=True, max_length=100)

    chapter_heading = models.CharField(
        blank=True,
        default="Introduction",
        help_text='Optional, e.g. "Introduction", chapter heading that will appear before the body',
        max_length=255,
    )
    body = StreamField(LongformStoryBlock())

    document = models.ForeignKey(
        settings.WAGTAILDOCS_DOCUMENT_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    document_link_text = models.CharField(
        blank=True,
        help_text='Optional, e.g. "Download the policy", defaults to the linked document\'s own title',
        max_length=255,
    )

    search_fields = BasePage.search_fields + [index.SearchField("body")]

    content_panels = BasePage.content_panels + [
        FieldPanel("last_updated"),
        FieldPanel("version_number"),
        MultiFieldPanel(
            [DocumentChooserPanel("document"), FieldPanel("document_link_text")],
            heading="Documents",
        ),
        FieldPanel("chapter_heading"),
        StreamFieldPanel("body"),
    ]

    @cached_property
    def previous_chapter(self):
        return None

    @cached_property
    def next_chapter(self):
        return self.get_children().live().specific().first()

    def get_index(self):
        return [self] + list(self.get_children().specific())


class LongformChapterPage(BasePage):
    template = "patterns/pages/longform/longform_page.html"
    subpage_types = []
    parent_page_types = ["LongformPage"]

    class Meta:
        verbose_name = "Long-form content chapter page"

    is_chapter_page = True

    body = StreamField(LongformStoryBlock())

    search_fields = BasePage.search_fields + [index.SearchField("body")]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel("body"),
    ]

    @cached_property
    def previous_chapter(self):
        return self.get_prev_siblings().specific().first() or self.get_parent().specific

    @cached_property
    def next_chapter(self):
        return self.get_next_siblings().specific().first()

    def get_index(self):
        return self.get_parent().specific.get_index()
