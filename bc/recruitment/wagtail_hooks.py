from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from bc.recruitment.models import TalentLinkJob


class TalentLinkJobModelAdmin(ModelAdmin):
    model = TalentLinkJob
    menu_icon = "tag"
    list_display = ("talentlink_id", "job_number", "title", "last_imported")


class RecruitmentModelAdminGroup(ModelAdminGroup):
    menu_label = "Recruitment"
    items = (TalentLinkJobModelAdmin,)
    menu_icon = "tag"


modeladmin_register(RecruitmentModelAdminGroup)
