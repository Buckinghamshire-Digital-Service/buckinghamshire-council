from django.test import TestCase

from bc.news.templatetags.news_tags import is_news_page
from bc.news.tests.fixtures import NewsPageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory


class TestIsNewsPageTag(TestCase):
    def test_false_for_info_page(self):
        page = InformationPageFactory.build()

        result = is_news_page(page)

        self.assertIs(result, False)

    def test_true_for_news_page(self):
        page = NewsPageFactory.build()

        result = is_news_page(page)

        self.assertIs(result, True)
