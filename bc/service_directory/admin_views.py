from wagtail.admin.ui.tables import BooleanColumn
from wagtail.admin.views.generic.models import IndexView
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup

from . import models


class DirectoryManagementAPIModelViewSet(ModelViewSet):
    copy_view_enabled = False
    icon = "cog"
    inspect_view_enabled = True
    list_display = ["admin_name", BooleanColumn("is_enabled"), "api_url"]
    list_filter = ["is_enabled"]
    menu_label = "Management APIs"
    model = models.DirectoryManagementAPI


directory_management_api_model_viewset = DirectoryManagementAPIModelViewSet(
    "service-directory/directory-management-apis"
)


class ServiceDirectoryModelViewSet(ModelViewSet):
    copy_view_enabled = False
    icon = "folder-open-inverse"
    inspect_view_enabled = True
    list_display = ["admin_name", "directory_api_slug", "directory_management_api"]
    list_filter = ["directory_management_api"]
    menu_label = "Directories"
    model = models.ServiceDirectory

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.is_searching:
            queryset = queryset.select_related("directory_management_api")
        return queryset


service_directory_model_viewset = ServiceDirectoryModelViewSet(
    "service-directory/service-directories"
)


class TaxonomyIndexView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.is_searching:
            queryset = queryset.select_related("fetched_with")
        return queryset


# TODO: Consider making TaxonomyModelViewSet read-only once upgraded to newer
#       Wagtail that supports ModelViewSet inspect views.
class TaxonomyModelViewSet(ModelViewSet):
    add_to_settings_menu = True
    copy_view_enabled = False
    icon = "tag"
    index_view_class = TaxonomyIndexView
    inspect_view_enabled = True
    list_filter = ["fetched_with", "level"]
    list_display = ["label", "remote_slug", "level", "fetched_with"]
    menu_label = "Taxonomies"
    model = models.Taxonomy


taxonomy_model_viewset = TaxonomyModelViewSet("service-directory/taxonomies")


class ServiceDirectoryModelViewSetGroup(ModelViewSetGroup):
    items = (
        directory_management_api_model_viewset,
        service_directory_model_viewset,
        taxonomy_model_viewset,
    )
    menu_label = "Service directory"
    menu_icon = "folder-open-inverse"
