from bc.utils.models import BasePage


class PromotionalHomePage(BasePage):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "promotional.PromotionalSiteConfiguration",
        "promotional.PromotionalContentPage",
    ]
    template = "patterns/pages/promotional/home_page.html"

    search_fields = BasePage.search_fields + []
    content_panels = BasePage.content_panels + []
