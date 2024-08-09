from typing import Optional

from bc.service_directory import api_schema
from bc.service_directory.resources import ManageDirectoryAPIResources

from .api_client import get_api_client_class
from .models import DirectoryManagementAPI, Taxonomy


class DirectoryManagementAPIIsNotEnabled(Exception):
    pass


def fetch_and_create_taxonomies(
    directory_management_api: DirectoryManagementAPI, /, *, api_timeout: Optional[float]
) -> None:
    if not directory_management_api.is_enabled:
        raise DirectoryManagementAPIIsNotEnabled(directory_management_api.pk)

    client = get_api_client_class()(
        base_url=directory_management_api.api_url, timeout=api_timeout
    )
    api_resource = ManageDirectoryAPIResources(client=client)

    for api_taxonomy in api_resource.get_taxonomies():
        created_taxonomy = _create_taxonomy(
            api_taxonomy=api_taxonomy,
            directory_management_api=directory_management_api,
            parent=None,
        )
        _traverse_children(
            api_taxonomy=api_taxonomy,
            directory_management_api=directory_management_api,
            parent=created_taxonomy,
        )


def _create_taxonomy(
    *,
    api_taxonomy: api_schema.Taxonomy,
    directory_management_api: DirectoryManagementAPI,
    parent: Optional[Taxonomy],
) -> Taxonomy:
    created_taxonomy = Taxonomy.objects.update_or_create(
        fetched_with=directory_management_api,
        remote_id=api_taxonomy.id,
        defaults={
            "label": api_taxonomy.label,
            "level": api_taxonomy.level,
            "parent": parent,
            "remote_slug": api_taxonomy.slug,
        },
    )[0]
    _traverse_children(
        api_taxonomy=api_taxonomy,
        directory_management_api=directory_management_api,
        parent=created_taxonomy,
    )
    return created_taxonomy


def _traverse_children(
    *,
    api_taxonomy: api_schema.Taxonomy,
    directory_management_api: DirectoryManagementAPI,
    parent: Optional[Taxonomy],
) -> None:
    for child in api_taxonomy.children:
        _create_taxonomy(
            api_taxonomy=child,
            directory_management_api=directory_management_api,
            parent=parent,
        )
