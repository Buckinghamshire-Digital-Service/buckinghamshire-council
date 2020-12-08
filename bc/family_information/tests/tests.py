from wagtail.tests.utils import WagtailPageTests

from ...standardpages.models import IndexPage, InformationPage
from ..models import CategoryTypeOnePage, CategoryTypeTwoPage


class CategoryTypePagesWagtailPageTests(WagtailPageTests):
    """
    Test page creation and infrastructure
    """

    def test_can_create_index_page_at_cat_pages(self):
        self.assertCanCreateAt(CategoryTypeOnePage, IndexPage)
        self.assertCanCreateAt(CategoryTypeTwoPage, IndexPage)

    def test_can_create_information_page_at_cat_pages(self):
        self.assertCanCreateAt(CategoryTypeOnePage, InformationPage)
        self.assertCanCreateAt(CategoryTypeTwoPage, InformationPage)
