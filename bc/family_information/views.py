from wagtail.admin.viewsets.chooser import ChooserViewSet


class EHCCoChooserViewSet(ChooserViewSet):
    model = "family_information.EHCCo"

    icon = "user"
    choose_one_text = "Choose an EHC Co"
    choose_another_text = "Choose another EHC Co"
    edit_item_text = "Edit this EHC Co"
    form_fields = ["name", "email"]
    url_filter_parameters = ["name", "email"]


ehc_co_chooser_viewset = EHCCoChooserViewSet("ehc_co_chooser")
