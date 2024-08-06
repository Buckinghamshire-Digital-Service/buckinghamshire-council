import datetime
import logging
from typing import Any, List, Mapping, Optional, Sequence, TypedDict

from django.utils import timezone
from django.utils.text import Truncator

from wagtail import blocks

from bc.service_directory import api_schema
from bc.service_directory.models import ServiceDirectory, Taxonomy
from bc.service_directory.resources import ServiceDirectoryAPIResources
from bc.service_directory.services import (
    format_service_detail_page_url,
    format_services_listing_page_url,
)

from . import admin_choosers, api_client

logger = logging.getLogger(__name__)


class _ServiceTag(TypedDict):
    highlight: bool
    title: str


class _ServiceContext(TypedDict):
    intro: str
    name: str
    url: str
    tags: List[_ServiceTag]


class _DirectoryServicesBlockContext(TypedDict):
    activities: Optional[Sequence[_ServiceContext]]
    heading: str


class CouldNotFetchActivities(Exception):
    pass


ServiceDirectoryChooserBlock = (
    admin_choosers.service_directory_chooser_viewset.get_block_class(
        name="ServiceDirectoryChooserBlock", module_path="bc.service_directory.blocks"
    )
)
TaxonomyChooserBlock = admin_choosers.taxonomy_chooser_viewset.get_block_class(
    name="TaxonomyChooserBlock", module_path="bc.service_directory.blocks"
)


class DirectoryServicesBlock(blocks.StructBlock):
    SERVICE_DESCRIPTION_CHARS = 106
    RECENTLY_UPDATED_TIMEDELTA: datetime.timedelta = datetime.timedelta(days=30)

    heading = blocks.CharBlock(required=False)
    service_directory = ServiceDirectoryChooserBlock()
    categories = blocks.ListBlock(TaxonomyChooserBlock())
    collection = TaxonomyChooserBlock(required=False)

    class Meta:
        icon = "calendar-alt"
        template = "patterns/molecules/streamfield/blocks/directory_services_block.html"

    def clean(self, value) -> Mapping[str, Any]:
        cleaned_data = super().clean(value)
        directory = cleaned_data.get("service_directory")
        categories = cleaned_data.get("categories", [])
        collection = cleaned_data.get("collection")

        errors = {}

        for category in categories:
            if category.fetched_with_directory != directory:
                errors["categories"].setdefault("fetched_with_directory", []).append(
                    "Categories must be fetched with the same directory as the service directory"
                )

        if collection is not None and collection.fetched_with_directory != directory:
            errors["collection"].setdefault("fetched_with_directory", []).append(
                "Collection must be fetched with the same directory as the service directory"
            )

        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)

        return cleaned_data

    def get_context(self, value, parent_context=None) -> _DirectoryServicesBlockContext:
        context = super().get_context(value, parent_context=parent_context)

        directory = value["service_directory"]
        categories = [c for c in value.get("categories", []) if c is not None]
        collection = value.get("collection")

        if directory is None:
            logger.warning(
                "Directory value is empty on a block. It might have been deleted."
            )
            return context

        try:
            context["activities"] = self.get_activities(
                directory=directory, categories=categories, collection=collection
            )
        except CouldNotFetchActivities:
            logger.exception("There was an issue fetching activities")
            context["activities"] = None

        context["view_all_activities_url"] = self.get_view_all_activities_url(
            categories=categories, collection=collection, directory=directory
        )
        context["heading"] = value.get("heading", "")
        return context

    @classmethod
    def get_activities(
        cls,
        *,
        directory: ServiceDirectory,
        categories: Sequence[Taxonomy],
        collection: Taxonomy,
    ) -> List[_ServiceContext]:
        client = api_client.get_api_client_class()(
            base_url=directory.directory_api_url,
        )
        api = ServiceDirectoryAPIResources(client=client)
        taxonomies = [category.remote_slug for category in categories]

        try:
            services = api.get_services(
                directories=[directory.directory_api_slug],
                taxonomies=taxonomies,
                per_page=4,
                page=1,
            )
        except api_client.ServiceDirectoryClientError as e:
            raise CouldNotFetchActivities from e

        # Context for building the URL.
        collection_filter = collection.remote_slug if collection is not None else None
        categories_filter = [category.remote_slug for category in categories]

        services_context: List[_ServiceContext] = []
        for service in services:
            tags: List[_ServiceTag] = []
            if service.local_offer:
                tags.append({"highlight": True, "title": "Part of local offer"})
            if service.free:
                tags.append({"highlight": False, "title": "Free"})
            if service.updated_at <= timezone.now() - cls.RECENTLY_UPDATED_TIMEDELTA:
                tags.append({"highlight": False, "title": "Recently updated"})

            url = format_service_detail_page_url(
                service,
                category_filters=categories_filter,
                collection_filter=collection_filter,
                frontend_url=directory.frontend_url,
            )

            service_context: _ServiceContext = {
                "intro": cls._format_activity_intro(service),
                "name": service.name,
                "url": url,
                "tags": tags,
            }
            services_context.append(service_context)
        return services_context

    @classmethod
    def _format_activity_intro(
        cls, service: api_schema.Service, /, *, max_length: Optional[int] = None
    ) -> str:
        """
        Shorten the description, and then remove the newlines.
        """
        if max_length is None:
            max_length = cls.SERVICE_DESCRIPTION_CHARS
        description = Truncator(service.description).chars(max_length)
        return " ".join(description.splitlines())

    @classmethod
    def get_view_all_activities_url(
        cls,
        *,
        directory: ServiceDirectory,
        categories: Sequence[Taxonomy],
        collection: Taxonomy,
    ) -> str:
        category_filters = [category.remote_slug for category in categories]
        collection_filter = collection.remote_slug if collection is not None else None
        return format_services_listing_page_url(
            category_filters=category_filters,
            collection_filter=collection_filter,
            frontend_url=directory.frontend_url,
        )
