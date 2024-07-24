from typing import Optional, Sequence
from urllib.parse import quote_plus

from django.http import QueryDict

from bc.service_directory.types import APIService, Category, Collection, Directory


def get_service_detail_page_url(
    service: APIService,
    /,
    *,
    category_filters: Optional[Sequence[Category]] = None,
    collection_filter: Optional[Collection] = None,
    directory: Directory,
):
    query_dict = QueryDict(mutable=True)

    if collection_filter is not None:
        query_dict["collection"] = collection_filter.value

    if category_filters is not None:
        for category in category_filters:
            query_dict.appendlist("categories", category.value)

    base_url = directory.frontend_url
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    url = f"{base_url}/service/{quote_plus(str(service.id))}"

    if query_dict:
        url += f"?{query_dict.urlencode()}"
    return url


def get_services_listing_page_url(
    *,
    category_filters: Optional[Sequence[Category]] = None,
    collection_filter: Optional[Collection] = None,
    directory: Directory,
):
    query_dict = QueryDict(mutable=True)

    if collection_filter is not None:
        query_dict["collection"] = collection_filter.value

    if category_filters is not None:
        for category in category_filters:
            query_dict.appendlist("categories", category.value)

    url = directory.frontend_url

    if query_dict:
        url += f"?{query_dict.urlencode()}"
    return url
