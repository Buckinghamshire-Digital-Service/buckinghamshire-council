from wagtail import hooks

from . import admin_choosers, admin_views


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
