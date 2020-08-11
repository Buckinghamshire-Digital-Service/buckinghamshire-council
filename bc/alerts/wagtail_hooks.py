from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from bc.alerts.models import Alert


class AlertModelAdmin(ModelAdmin):
    model = Alert
    menu_icon = "warning"
    list_display = ("title", "page")


modeladmin_register(AlertModelAdmin)
