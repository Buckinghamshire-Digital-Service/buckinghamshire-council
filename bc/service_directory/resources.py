from typing import List, Sequence, cast

from .client import BaseOutpostClient
from .types import APIService, Category, Directory


class ServiceDirectoryResources:
    client: BaseOutpostClient

    def __init__(self, *, client: BaseOutpostClient):
        self.client = client

    def get_services(
        self,
        *,
        directories: Sequence[Directory],
        taxonomies: Sequence[Category],
        per_page: int,
        page: int
    ) -> List[APIService]:
        """
        https://github.com/wearefuturegov/outpost-api-service/wiki/Search-services
        """
        service_schema = APIService.schema()
        response = self.client.get(
            "services",
            params={
                "directories": ",".join(
                    directory.api_value for directory in directories
                ),
                "taxonomies": ",".join(taxonomy.api_value for taxonomy in taxonomies),
                "per_page": str(per_page),
                "page": str(page),
            },
        )
        services = service_schema.load(response["content"], many=True)
        return cast(List[APIService], services)
