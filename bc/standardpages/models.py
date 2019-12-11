from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class InformationPageRelatedPage(RelatedPage):
    source_page = ParentalKey("InformationPage", related_name="related_pages")


class InformationPage(BasePage):
    template = "patterns/pages/standardpages/information_page.html"

    body = StreamField(StoryBlock())

    search_fields = BasePage.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]


class IndexPage(BasePage):
    template = "patterns/pages/standardpages/index_page.html"

    introduction = models.TextField(blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("introduction")]

    search_fields = BasePage.search_fields + [index.SearchField("introduction")]

    @cached_property
    def featured_pages(self):
        return self.get_children().live().public().order_by("path")[:3]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        subpages = self.get_children().live()
        per_page = settings.DEFAULT_PER_PAGE
        page_number = request.GET.get("page")
        paginator = Paginator(subpages, per_page)

        try:
            subpages = paginator.page(page_number)
        except PageNotAnInteger:
            subpages = paginator.page(1)
        except EmptyPage:
            subpages = paginator.page(paginator.num_pages)

        context["subpages"] = subpages

        return context
