from typing import List, Sequence, cast

from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from . import api_schema
from .api_client import BaseServiceDirectoryClient


class ServiceDirectoryValidationError(Exception):
    pass


class BaseResources:
    client: BaseServiceDirectoryClient

    def __init__(self, *, client: BaseServiceDirectoryClient):
        self.client = client


class ServiceDirectoryAPIResources(BaseResources):
    def get_services(
        self,
        *,
        directories: Sequence[str],
        taxonomies: Sequence[str],
        per_page: int,
        page: int
    ) -> List[api_schema.Service]:
        """
        https://github.com/wearefuturegov/outpost-api-service/wiki/Search-services
        """
        service_schema = api_schema.Service.schema()
        response = self.client.get(
            "services",
            params={
                "directories": ",".join(directories),
                "taxonomies": ",".join(taxonomies),
                "per_page": str(per_page),
                "page": str(page),
            },
        )
        if "content" not in response:
            raise ServiceDirectoryValidationError("Missing 'content' key in response")
        try:
            services = service_schema.load(response["content"], many=True)
        except MarshmallowValidationError as e:
            raise ServiceDirectoryValidationError from e
        return cast(List[api_schema.Service], services)


class ManageDirectoryAPIResources(BaseResources):
    def get_taxonomies(self) -> List[api_schema.Taxonomy]:
        taxonomy_schema = api_schema.Taxonomy.schema()
        response = self.client.get("taxonomies")
        services = taxonomy_schema.load(response, many=True)
        return cast(List[api_schema.Taxonomy], services)
