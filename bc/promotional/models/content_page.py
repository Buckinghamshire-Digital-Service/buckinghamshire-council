from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from bc.utils.models import BasePage

from ..blocks.definition import PromotionalStoryBlock


class PromotionalContentPage(BasePage):
    parent_page_types = [
        "promotional.PromotionalHomePage",
        "promotional.PromotionalContentPage",
    ]
    subpage_types = ["promotional.PromotionalContentPage"]

    template = "patterns/pages/promotional/content_page.html"

    body = StreamField(PromotionalStoryBlock())

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]
