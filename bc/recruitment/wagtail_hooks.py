from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from bc.recruitment.models import TalentLinkJob


class TalentLinkJobModelAdmin(ModelAdmin):
    model = TalentLinkJob
    menu_icon = "tag"
    list_display = (
        "talentlink_id",
        "job_number",
        "job_link",
        "title",
        "get_categories_list",
        "last_imported",
    )

    def job_link(self, obj):
        return format_html('<a href="{}">{}</span>', obj.url, obj.title,)


class RecruitmentModelAdminGroup(ModelAdminGroup):
    menu_label = "Recruitment"
    items = (TalentLinkJobModelAdmin,)
    menu_icon = "tag"


modeladmin_register(RecruitmentModelAdminGroup)
