from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

import wagtail
from wagtail import hooks

from . import admin_choosers, admin_views, models


@hooks.register("register_admin_viewset")
def register_directory_management_api_chooser_viewset():
    return admin_choosers.directory_management_api_chooser_viewset


@hooks.register("register_admin_viewset")
def register_service_directory_chooser_viewset():
    return admin_choosers.service_directory_chooser_viewset


@hooks.register("register_admin_viewset")
def register_taxonomy_chooser_viewset():
    return admin_choosers.taxonomy_chooser_viewset


@hooks.register("register_admin_viewset")
def register_service_directory_model_viewset_group():
    return admin_views.ServiceDirectoryModelViewSetGroup()


if wagtail.VERSION >= (6, 2):
    raise Exception(
        "ModelViewSet permissions should be registered automatically on Wagtail 6.2. "
        "Please re-test if they do in the groups."
    )


@hooks.register("register_permissions")
def register_service_directory_permissions():
    content_types = ContentType.objects.get_for_models(
        models.DirectoryManagementAPI, models.ServiceDirectory, models.Taxonomy
    ).values()
    return Permission.objects.filter(content_type__in=content_types)
