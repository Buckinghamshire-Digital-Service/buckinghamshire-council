from django.utils.html import format_html
from wagtail.search.utils import OR
from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from bc.recruitment.models import JobAlertSubscription, TalentLinkJob


class TalentLinkJobModelAdmin(ModelAdmin):
    model = TalentLinkJob
    menu_icon = "tag"
    list_display = (
        "homepage",
        "talentlink_id",
        "job_number",
        "job_link",
        "title",
        "get_categories_list",
        "last_imported",
        "location_postcode",
    )
    search_fields = ("talentlink_id", "job_number", "title")
    list_filter = ("homepage",)
    extra_search_kwargs = {"operator": OR}

    def job_link(self, obj):
        return format_html(
            '<a href="{}">{}</span>',
            obj.url,
            obj.title,
        )


class JobAlertSubscriptionModelAdmin(ModelAdmin):
    model = JobAlertSubscription
    menu_icon = "tag"
    list_display = ("homepage", "email", "confirmed", "created", "search", "token")
    search_fields = ("email", "search")
    list_filter = ("confirmed", "created", "homepage")
    extra_search_kwargs = {"operator": OR}


class RecruitmentModelAdminGroup(ModelAdminGroup):
    menu_label = "Recruitment"
    items = (
        TalentLinkJobModelAdmin,
        JobAlertSubscriptionModelAdmin,
    )
    menu_icon = "tag"


modeladmin_register(RecruitmentModelAdminGroup)
