from ..utils.models import BasePage


class PromotionalHomePage(BasePage):
    parent_page_types = ["wagtailcore.Page"]
    template = "patterns/pages/promotional/home_page.html"

    search_fields = BasePage.search_fields + []
    content_panels = BasePage.content_panels + []
