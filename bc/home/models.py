import json

from django.db import models
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel
from wagtail.search import index

from ..events.models import EventIndexPage
from ..news.models import NewsIndex
from ..standardpages.models import IndexPage
from ..utils.models import BasePage


class HomePage(BasePage):
    template = "patterns/pages/home/home_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    strapline = models.CharField(
        max_length=255, help_text="eg. Welcome to Buckinghamshire"
    )
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    logo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="For search engines and schema.org markup",
    )

    search_fields = BasePage.search_fields + [index.SearchField("strapline")]

    content_panels = BasePage.content_panels + [
        FieldPanel("strapline"),
        FieldPanel("hero_image"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = BasePage.promote_panels + [
        FieldPanel("logo"),
    ]

    @cached_property
    def child_sections(self):
        """
        Returns queryset of this page's live, public children that are of IndexPage class
        Ordered by Wagtail explorer custom sort (ie. path)
        """
        return (
            IndexPage.objects.child_of(self)
            .filter(show_in_menus=True)
            .live()
            .public()
            .order_by("path")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        try:
            news_index = NewsIndex.objects.live().public().first()
            context["news_index"] = news_index
            context["latest_news"] = news_index.news_pages[:3]
        except AttributeError:
            # No news index, ignore
            pass

        try:
            event_index = EventIndexPage.objects.live().public().first()
            context["event_index"] = event_index
            context["latest_events"] = event_index.upcoming_events[:3]
        except AttributeError:
            # No event index, ignore
            pass

        sections = self.child_sections
        context["sections"] = sections

        return context

    @property
    def schema_org_markup(self):
        markup = {
            "@context": "https://schema.org",
            "@type": "GovernmentOrganization",
            "name": "Buckinghamshire Council",
            "legalName": "Buckinghamshire Council",
            "url": "https://www.buckinghamshire.gov.uk/",
            "foundingDate": "2020",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "The Gateway, Gatehouse Road",
                "addressLocality": "Aylesbury",
                "addressRegion": "Buckinghamshire",
                "postalCode": "HP19 8FF",
                "addressCountry": "UK",
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "Support",
                "telephone": "[+443001316000]",
            },
            "areaServed": {"@type": "AdministrativeArea", "name": "Buckinghamshire"},
            "sameAs": [
                "https://www.facebook.com/BucksCouncil/",
                "https://twitter.com/buckscouncil",
                "https://www.linkedin.com/company/buckinghamshire-council",
            ],
        }

        if self.logo:
            markup["logo"] = self.logo.get_rendition("max-250x250").url

        return mark_safe(json.dumps(markup))
