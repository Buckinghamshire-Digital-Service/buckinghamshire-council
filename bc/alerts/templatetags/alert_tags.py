from django import template

from bc.alerts.models import Alert

register = template.Library()


@register.simple_tag
def get_alerts(page):
    return Alert.get_alerts_for_page(page)
