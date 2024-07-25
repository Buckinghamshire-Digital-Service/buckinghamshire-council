from wagtail.admin.viewsets.chooser import ChooserViewSet

from . import models


class ServiceDirectoryChooserViewSet(ChooserViewSet):
    choose_another_text = "Choose a directory"
    choose_one_text = "Choose a directory"
    edit_item_text = "Edit this directory"
    icon = "folder-open-inverse"
    model = models.ServiceDirectory


service_directory_chooser_viewset = ServiceDirectoryChooserViewSet(
    "service-directory-chooser"
)


class TaxonomyChooserViewSet(ChooserViewSet):
    choose_another_text = "Choose a taxonomy"
    choose_one_text = "Choose a taxonomy"
    edit_item_text = "Edit this taxonomy"
    icon = "tag"
    model = models.Taxonomy
    per_page = 50

    def get_object_list(self):
        return self.model.objects.select_related("fetched_with_directory")


taxonomy_chooser_viewset = TaxonomyChooserViewSet("service-directory-taxonomy-chooser")
