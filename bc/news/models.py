from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class NewsType(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class NewsPageNewsType(models.Model):
    page = ParentalKey("news.NewsPage", related_name="news_types")
    news_type = models.ForeignKey(
        "NewsType", related_name="+", on_delete=models.CASCADE
    )

    panels = [FieldPanel("news_type")]

    def __str__(self):
        return self.news_type.title


class NewsPageRelatedPage(RelatedPage):
    source_page = ParentalKey("news.NewsPage", related_name="related_pages")


class NewsPage(BasePage):
    template = "patterns/pages/news/news_page.html"

    subpage_types = []
    parent_page_types = ["NewsIndex"]

    # It's datetime for easy comparison with first_published_at
    publication_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Use this field to override the date that the "
        "news item appears to have been published.",
    )
    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("introduction"),
        FieldPanel("body"),
        InlinePanel("news_types", label="News types"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    @property
    def display_date(self):
        if self.publication_date:
            return self.publication_date
        else:
            return self.first_published_at

    @cached_property
    def live_related_pages(self):
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]


class NewsIndex(BasePage):
    template = "patterns/pages/news/news_index.html"

    subpage_types = ["NewsPage"]
    parent_page_types = ["home.HomePage", "family_information.SubsiteHomePage"]

    @cached_property
    def news_pages(self):
        news = (
            NewsPage.objects.live()
            .public()
            .descendant_of(self)
            .annotate(date=Coalesce("publication_date", "first_published_at"))
            .order_by("-date")
        )
        return news

    def get_context(self, request, *args, **kwargs):
        news = self.news_pages

        if request.GET.get("news_type"):
            news = news.filter(news_types__news_type=request.GET.get("news_type"))

        # Pagination
        page = request.GET.get("page", 1)
        paginator = Paginator(news, settings.DEFAULT_PER_PAGE)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            news=news,
            # Only show news types that have been used
            news_types=NewsPageNewsType.objects.all()
            .values_list("news_type__pk", "news_type__title")
            .distinct()
            .order_by("news_type__title"),
        )
        return context
