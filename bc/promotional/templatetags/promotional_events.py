import logging
from typing import Optional, Sequence, TypedDict

from django import template
from django.db.models import prefetch_related_objects

from wagtail.models import Site

from bc.events.templatetags.event_tags import format_event_date
from bc.images.models import CustomImage

from .. import utils

logger = logging.getLogger(__name__)

register = template.Library()


class EventContext(TypedDict):
    title: str
    date: str
    location: str
    summary: str
    image: Optional[CustomImage]
    url: str


class UpcomingEventsContext(TypedDict):
    visible: bool
    events: Sequence[EventContext]
    view_all_url: Optional[str]


# Promotional primary navigation
@register.inclusion_tag(
    "patterns/organisms/promotional-upcoming-events/promotional-upcoming-events.html",
    takes_context=True,
)
def upcoming_events(context) -> UpcomingEventsContext:
    request = context["request"]
    current_site = Site.find_for_request(request)

    try:
        site_config = utils.get_promotional_site_configuration(current_site)
    except utils.PromotionalSiteConfigurationDoesNotExist:
        logger.exception(
            "Failed to get promotional site configuration for site_pk=%s.",
            current_site.pk,
        )
        return {"visible": False, "events": [], "view_all_url": None}

    events_index = site_config.events_feed
    if events_index is None:
        return {"visible": False, "events": [], "view_all_url": None}

    events_index = events_index.specific

    events = events_index.upcoming_events[:4]
    prefetch_related_objects(
        events, "event_types__event_type", "listing_image__renditions"
    )

    events_context: Sequence[EventContext] = []

    for event in events:
        events_context.append(
            {
                "title": event.listing_title or event.title,
                "date": format_event_date(event.start_date, None, event.end_date, None),
                "summary": event.listing_summary or event.introduction,
                "image": event.listing_image,
                "location": event.location_name,
                "url": event.get_url(request=request),
            }
        )

    return {
        "visible": True,
        "events": events_context,
        "view_all_url": events_index.get_url(request=request),
    }
