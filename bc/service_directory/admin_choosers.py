from wagtail.admin.viewsets.chooser import ChooserViewSet

from . import models


class ServiceDirectoryChooserViewSet(ChooserViewSet):
    choose_another_text = "Choose a directory"
    choose_one_text = "Choose a directory"
    edit_item_text = "Edit this directory"
    icon = "folder-open-inverse"
    model = models.ServiceDirectory


service_directory_chooser_viewset = ServiceDirectoryChooserViewSet(
    "service-directory/directory-chooser"
)


class TaxonomyChooserViewSet(ChooserViewSet):
    choose_another_text = "Choose a taxonomy"
    choose_one_text = "Choose a taxonomy"
    edit_item_text = "Edit this taxonomy"
    icon = "tag"
    model = models.Taxonomy
    per_page = 50

    def get_object_list(self):
        return self.model.objects.select_related("fetched_with")


taxonomy_chooser_viewset = TaxonomyChooserViewSet("service-directory/taxonomy-chooser")


class DirectoryManagementAPIChooserViewSet(ChooserViewSet):
    choose_another_text = "Choose a management API"
    choose_one_text = "Choose a management API"
    edit_item_text = "Edit this management API"
    icon = "cog"
    model = models.DirectoryManagementAPI


directory_management_api_chooser_viewset = DirectoryManagementAPIChooserViewSet(
    "service-directory/directory-management-api-chooser"
)
