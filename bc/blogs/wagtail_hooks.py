from wagtail import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.models import PageLogEntry

from bc.blogs.models import BlogAlertSubscription, BlogPostPage, NotificationRecord


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
    if (
        PageLogEntry.objects.filter(page=page, action__exact="wagtail.publish").count()
        == 1
    ):
        if request.method == "POST" and page.specific_class == BlogPostPage:
            NotificationRecord(blog_post=page).save()
