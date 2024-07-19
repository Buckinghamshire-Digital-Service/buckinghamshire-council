from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

from dataclasses_json import dataclass_json

from .client import BaseOutpostClient
from .types import Directory, Taxonomy


@dataclass_json
@dataclass
class Service:
    id: int
    name: str


class ServiceDirectoryResources:
    client: BaseOutpostClient

    def __init__(self, *, client: BaseOutpostClient):
        self.client = client

    def get_services(
        self,
        *,
        directories: Sequence[Directory],
        taxonomies: Sequence[Taxonomy],
        per_page: int,
        page: int
    ) -> list[Service]:
        """
        https://github.com/wearefuturegov/outpost-api-service/wiki/Search-services
        """
        service_schema = Service.schema()
        response = self.client.get(
            "services",
            params={
                "directories": ",".join(directory.value for directory in directories),
                "taxonomies": ",".join(taxonomy.value for taxonomy in taxonomies),
                "per_page": str(per_page),
                "page": str(page),
            },
        )
        services = service_schema.load(response["content"], many=True)
        return cast(list[Service], services)
