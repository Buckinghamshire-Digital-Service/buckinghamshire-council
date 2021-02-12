from django.test import TestCase, override_settings

from wagtail.core.models import Page

from bc.news.tests.fixtures import NewsPageFactory
from bc.home.models import HomePage
from .utils import get_search_settings_for_test, update_search_index


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class TestNewsSearchBoostReduction(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def create_news_page(self):
        news_page = NewsPageFactory.build(title="Hammer")
        self.homepage.add_child(instance=news_page)
        self.news_page = Page.objects.get(pk=news_page.id)

    def test_news_page_in_search_results(self):
        self.create_news_page()
        update_search_index()

        search_results = Page.objects.search("Hammer")

        self.assertEqual(self.news_page, list(search_results)[0])

