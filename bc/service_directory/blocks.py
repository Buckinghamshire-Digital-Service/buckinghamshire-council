import datetime
import logging
from typing import List, Optional, Sequence, TypedDict

from django.utils import timezone
from django.utils.text import Truncator

from wagtail import blocks

from bc.service_directory.resources import ServiceDirectoryResources
from bc.service_directory.services import (
    get_service_detail_page_url,
    get_services_listing_page_url,
)

from .client import ClientError, RequestsClient
from .types import APIService, Category, Directory

logger = logging.getLogger(__name__)


class _ActivityTag(TypedDict):
    highlight: bool
    title: str


class _ActivityContext(TypedDict):
    intro: str
    name: str
    url: str
    tags: List[_ActivityTag]


class DirectoryActivitiesBlockContext(TypedDict):
    activities: Optional[Sequence[_ActivityContext]]
    heading: str


class CouldNotFetchActivities(Exception):
    pass


class DirectoryActivitiesBlock(blocks.StructBlock):
    SERVICE_DESCRIPTION_CHARS = 106

    heading = blocks.CharBlock(required=False)
    directory = blocks.ChoiceBlock(choices=Directory.get_choices())
    category = blocks.ChoiceBlock(choices=Category.get_choices())

    class Meta:
        template = (
            "patterns/molecules/streamfield/blocks/directory_activities_block.html"
        )

    def get_context(
        self, value, parent_context=None
    ) -> DirectoryActivitiesBlockContext:
        context = super().get_context(value, parent_context=parent_context)

        try:
            directory = Directory(value["directory"])
        except ValueError:
            logger.warning("Invalid directory value", exc_info=True)
            return context

        try:
            category = Category(value["category"])
        except ValueError:
            logger.warning("Invalid category value", exc_info=True)
            return context

        try:
            context["activities"] = self.get_activities(
                directory=directory, category=category
            )
        except CouldNotFetchActivities:
            logger.exception("There was an issue fetching activities")
            context["activities"] = None

        context["view_all_activities_url"] = get_services_listing_page_url(
            category_filters=[category],
            collection_filter=category.collection,
            directory=directory,
        )
        context["heading"] = value.get("heading", "")
        return context

    @classmethod
    def get_activities(
        cls, *, directory: Directory, category: Category
    ) -> List[_ActivityContext]:
        # TODO: Make client class and parameters configurable.
        client = RequestsClient(
            base_url=directory.api_url,
        )
        api = ServiceDirectoryResources(client=client)

        try:
            services = api.get_services(
                directories=[directory], taxonomies=[category], per_page=4, page=1
            )
        except ClientError as e:
            raise CouldNotFetchActivities from e

        activities_context: List[_ActivityContext] = []
        for service in services:
            tags: List[_ActivityTag] = []
            if service.local_offer:
                tags.append({"highlight": True, "title": "Part of local offer"})
            if service.free:
                tags.append({"highlight": False, "title": "Free"})
            if service.updated_at <= timezone.now() + datetime.timedelta(days=2):
                tags.append({"highlight": False, "title": "Recently updated"})

            activity_context: _ActivityContext = {
                "intro": cls._format_activity_intro(service),
                "name": service.name,
                "url": get_service_detail_page_url(
                    service,
                    category_filters=[category],
                    collection_filter=category.collection,
                    directory=directory,
                ),
                "tags": tags,
            }
            activities_context.append(activity_context)
        return activities_context

    @classmethod
    def _format_activity_intro(
        cls, service: APIService, /, *, max_length: Optional[int] = None
    ) -> str:
        """
        Shorten the description, and then remove the newlines.
        """
        if max_length is None:
            max_length = cls.SERVICE_DESCRIPTION_CHARS
        description = Truncator(service.description).chars(max_length)
        return " ".join(description.splitlines())
