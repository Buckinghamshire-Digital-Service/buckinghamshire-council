from wagtail.admin.ui.tables import BooleanColumn
from wagtail.admin.views.generic.models import IndexView
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup

from . import models


class ServiceDirectoryModelViewSet(ModelViewSet):
    copy_view_enabled = False
    icon = "folder-open-inverse"
    inspect_view_enabled = True
    list_display = ["admin_name", BooleanColumn("is_enabled"), "directory_api_slug"]
    list_filter = ["is_enabled"]
    menu_label = "Directories"
    model = models.ServiceDirectory


service_directory_model_viewset = ServiceDirectoryModelViewSet("service-directory")


class TaxonomyIndexView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.is_searching:
            queryset = queryset.select_related("fetched_with_directory")
        return queryset


class TaxonomyModelViewSet(ModelViewSet):
    add_to_settings_menu = True
    copy_view_enabled = False
    icon = "tag"
    index_view_class = TaxonomyIndexView
    inspect_view_enabled = True
    list_filter = ["fetched_with_directory", "level"]
    list_display = ["label", "remote_slug", "level", "fetched_with_directory"]
    menu_label = "Taxonomies"
    model = models.Taxonomy


taxonomy_model_viewset = TaxonomyModelViewSet("service-directory-taxonomy")


class ServiceDirectoryModelViewSetGroup(ModelViewSetGroup):
    items = (service_directory_model_viewset, taxonomy_model_viewset)
    menu_label = "Service Directory"
    menu_icon = "folder-open-inverse"
