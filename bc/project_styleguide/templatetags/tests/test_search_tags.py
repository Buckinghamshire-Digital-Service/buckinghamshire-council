from django.test import TestCase

from bc.home.models import HomePage
from bc.news.tests.fixtures import NewsPageFactory
from bc.project_styleguide.templatetags.search_tags import is_news_page
from bc.standardpages.tests.fixtures import InformationPageFactory


class TestIsNewsPageTag(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_false_for_info_page(self):
        page = InformationPageFactory.build()
        self.homepage.add_child(instance=page)

        result = is_news_page(page)

        self.assertIs(result, False)

    def test_true_for_news_page(self):
        page = NewsPageFactory.build()
        self.homepage.add_child(instance=page)

        result = is_news_page(page)

        self.assertIs(result, True)
