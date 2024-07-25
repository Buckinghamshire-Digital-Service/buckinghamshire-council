from typing import Optional, Sequence
from urllib.parse import quote_plus

from django.http import QueryDict

from . import api_schema


def format_service_detail_page_url(
    service: api_schema.Service,
    /,
    *,
    category_filters: Optional[Sequence[str]] = None,
    collection_filter: Optional[str] = None,
    frontend_url: str,
):
    query_dict = QueryDict(mutable=True)

    if collection_filter is not None:
        query_dict["collection"] = collection_filter

    if category_filters is not None:
        for category in category_filters:
            query_dict.appendlist("categories", category)

    if frontend_url.endswith("/"):
        frontend_url = frontend_url[:-1]

    url = f"{frontend_url}/service/{quote_plus(str(service.id))}"

    if query_dict:
        url += f"?{query_dict.urlencode()}"
    return url


def format_services_listing_page_url(
    *,
    category_filters: Optional[Sequence[str]] = None,
    collection_filter: Optional[str] = None,
    frontend_url: str,
):
    query_dict = QueryDict(mutable=True)

    if collection_filter is not None:
        query_dict["collection"] = collection_filter

    if category_filters is not None:
        for category in category_filters:
            query_dict.appendlist("categories", category)

    if query_dict:
        frontend_url += f"?{query_dict.urlencode()}"
    return frontend_url
