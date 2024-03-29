from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from bc.alerts.models import Alert


class AlertModelAdmin(ModelAdmin):
    model = Alert
    menu_icon = "warning"
    list_display = ("title", "alert_level", "page")
    search_fields = ["title", "page__title"]


modeladmin_register(AlertModelAdmin)
