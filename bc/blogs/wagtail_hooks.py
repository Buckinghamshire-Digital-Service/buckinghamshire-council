from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.core.models import PageLogEntry

import django_rq

from bc.blogs.models import BlogAlertSubscription, BlogPostPage
from bc.blogs.utils import alert_subscribed_users


class BlogAlertSubscriptionModelAdmin(ModelAdmin):
    model = BlogAlertSubscription
    menu_icon = "tag"
    list_display = ("homepage", "email", "confirmed", "created", "token")
    list_filter = ("confirmed", "created", "homepage")


class BlogModelAdminGroup(ModelAdminGroup):
    menu_label = "Blogs"
    items = [BlogAlertSubscriptionModelAdmin]
    menu_icon = "tag"


modeladmin_register(BlogModelAdminGroup)


@hooks.register("after_publish_page")
def send_emails(request, page):
    # only send notifications when a page is first published
    if PageLogEntry.objects.filter(page=page, action__exact="wagtail.publish").count() == 1:
        if request.method == "POST" and page.specific_class == BlogPostPage:
            django_rq.enqueue(alert_subscribed_users, page.pk)
