from django import template
from django.db.models import Q

from bc.alerts.models import Alert

register = template.Library()


@register.simple_tag
def get_alerts(page):
    return Alert.objects.filter(
        Q(page__in=page.get_ancestors(), show_on=Alert.PAGE_AND_DESCENDANTS)
        | Q(page=page)
    ).order_by("page__path")
