from collections import defaultdict

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from bc.utils.blocks import StoryBlock
from bc.utils.models import BasePage, RelatedPage


class EventType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class EventPageRelatedPage(RelatedPage):
    source_page = ParentalKey("events.EventPage", related_name="related_pages")


class EventPageEventType(models.Model):
    event_type = models.ForeignKey("events.EventType", on_delete=models.CASCADE)
    page = ParentalKey("events.EventPage", related_name="event_types")

    panels = [FieldPanel("event_type")]

    def __str__(self):
        return self.event_type.title


class EventPage(BasePage):
    template = "patterns/pages/events/event_page.html"

    subpage_types = []
    parent_page_types = ["EventIndexPage"]

    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    # Permit null=True on end_date, as we use Coalesce to query 'end_date or start_date'
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    location_name = models.CharField(_("Location name"), max_length=255)
    street_address_1 = models.CharField(
        _("Street Address 1"), blank=True, max_length=255
    )
    street_address_2 = models.CharField(
        _("Street Address 2"), blank=True, max_length=255
    )
    city = models.CharField(_("City"), blank=True, max_length=255)
    region = models.CharField(_("State or county"), blank=True, max_length=255)
    postcode = models.CharField(_("Zip or postal code"), blank=True, max_length=255)
    country = models.CharField(_("Country"), blank=True, max_length=255)

    introduction = models.TextField(blank=True)
    body = StreamField(StoryBlock())

    search_fields = BasePage.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("start_date"), FieldPanel("start_time")])],
            heading="Start",
        ),
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("end_date"), FieldPanel("end_time")])],
            heading="End",
        ),
        InlinePanel("event_types", label="Event types"),
        MultiFieldPanel(
            [
                FieldPanel("location_name"),
                FieldPanel("street_address_1"),
                FieldPanel("street_address_2"),
                FieldPanel("city"),
                FieldPanel("region"),
                FieldPanel("postcode"),
                FieldPanel("country"),
            ],
            _("Location"),
        ),
        FieldPanel("introduction"),
        FieldPanel("body"),
        InlinePanel("related_pages", label="Related pages"),
    ]

    @property
    def display_date(self):
        if self.start_date:
            return self.start_date

    @cached_property
    def live_related_pages(self):
        pages = self.related_pages.prefetch_related("page", "page__view_restrictions")
        return [
            related_page
            for related_page in pages
            if related_page.page.live
            and len(related_page.page.view_restrictions.all()) == 0
        ]

    @property
    def location(self):
        if self.location_name:
            return self.location_name

    def clean_fields(self, exclude=None):
        errors = defaultdict(list)
        try:
            super().clean_fields(exclude)
        except ValidationError as e:
            errors.update(e.message_dict)

        # Require start time if there's an end time
        if self.end_time and not self.start_time:
            errors["start_time"].append(
                _("If you enter an end time, you must also enter a start time")
            )

        if self.end_date and self.end_date < self.start_date:
            errors["end_date"].append(
                _("Events involving time travel are not supported")
            )
        elif (
            self.end_date == self.start_date
            and self.end_time
            and self.end_time < self.start_time
        ):
            errors["end_time"].append(
                _("Events involving time travel are not supported")
            )

        if errors:
            raise ValidationError(errors)


class EventIndexPage(BasePage):
    template = "patterns/pages/events/event_index_page.html"

    subpage_types = ["EventPage"]
    parent_page_types = ["home.HomePage", "family_information.SubsiteHomePage"]

    def _annotated_descendant_events(self):
        return (
            EventPage.objects.live()
            .public()
            .descendant_of(self)
            .annotate(latest_date=Coalesce("end_date", "start_date"))
        )

    @cached_property
    def upcoming_events(self):
        return (
            self._annotated_descendant_events()
            .filter(latest_date__gte=timezone.now().date())
            .order_by("start_date")
        )

    @cached_property
    def past_events(self):
        return (
            self._annotated_descendant_events()
            .filter(latest_date__lt=timezone.now().date())
            .order_by("-start_date")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        past_events = self.past_events
        upcoming_events = self.upcoming_events

        past = request.GET.get("past", False)
        if past:
            events = past_events
        else:
            events = upcoming_events
        per_page = settings.DEFAULT_PER_PAGE
        page_number = request.GET.get("page")
        paginator = Paginator(events, per_page)

        try:
            events = paginator.page(page_number)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context.update(
            {
                "show_past": past,
                "events": events,
                "past_events": past_events,
                "upcoming_events": upcoming_events,
            }
        )

        if past:
            context["extra_url_params"] = urlencode({"past": True})

        return context
