import logging

from wagtail.core import blocks

from bc.service_directory.resources import Service, ServiceDirectoryResources

from .client import RequestsClient
from .types import Directory, Taxonomy

logger = logging.getLogger(__name__)


class DirectoryActivitiesBlock(blocks.StructBlock):
    directory = blocks.ChoiceBlock(choices=Directory.choices)
    taxonomy = blocks.ChoiceBlock(choices=Taxonomy.choices)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            taxonomy = Taxonomy(value["taxonomy"])
        except ValueError:
            logger.warning("Invalid taxonomy value", exc_info=True)
            return context

        try:
            directory = Directory(value["directory"])
        except ValueError:
            logger.warning("Invalid directory value", exc_info=True)
            return context

        context["activities"] = self.get_activities(
            directory=directory, taxonomy=taxonomy
        )
        return context

    def get_activities(
        self, *, directory: Directory, taxonomy: Taxonomy
    ) -> list[Service]:
        # TODO: Make client class and parameters configurable.
        client = RequestsClient(
            base_url="https://api.familyinfo.buckinghamshire.gov.uk/api/v1/"
        )
        api = ServiceDirectoryResources(client=client)
        return api.get_services(
            directories=[directory], taxonomies=[taxonomy], per_page=4, page=1
        )
