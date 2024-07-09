from wagtail import hooks

from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from bc.family_information.models import EHCCo, School
from bc.family_information.views import ehc_co_chooser_viewset


class EHCCoModelAdmin(ModelAdmin):
    model = EHCCo
    menu_icon = "user"
    list_display = ("name", "email")
    search_fields = ("name", "email")


class SchoolModelAdmin(ModelAdmin):
    model = School
    menu_icon = "tag"
    list_display = ("name", "hub_email", "ehc_co")
    list_filter = ("hub_email", "ehc_co")


class SchoolsAdminGroup(ModelAdminGroup):
    menu_label = "Schools"
    items = [SchoolModelAdmin, EHCCoModelAdmin]
    menu_icon = "tag"


modeladmin_register(SchoolsAdminGroup)


@hooks.register("register_admin_viewset")
def register_viewset():
    return ehc_co_chooser_viewset
