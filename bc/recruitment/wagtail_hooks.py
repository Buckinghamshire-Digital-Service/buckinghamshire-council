from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from bc.recruitment.models import JobAlertSubscription, TalentLinkJob


class TalentLinkJobModelAdmin(ModelAdmin):
    model = TalentLinkJob
    menu_icon = "tag"
    list_display = (
        "talentlink_id",
        "job_number",
        "title",
        "get_categories_list",
        "last_imported",
    )


class JobAlertSubscriptionModelAdmin(ModelAdmin):
    model = JobAlertSubscription
    menu_icon = "tag"
    list_display = ("email", "confirmed", "created", "search")


class RecruitmentModelAdminGroup(ModelAdminGroup):
    menu_label = "Recruitment"
    items = (
        TalentLinkJobModelAdmin,
        JobAlertSubscriptionModelAdmin,
    )
    menu_icon = "tag"


modeladmin_register(RecruitmentModelAdminGroup)
