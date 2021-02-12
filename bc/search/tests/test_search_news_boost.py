import unittest

from django.test import TestCase, override_settings

from wagtail.core.models import Page
from wagtail.search.backends import get_search_backend

from bc.news.tests.fixtures import NewsPageFactory
from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory
from .utils import (
    get_search_settings_for_test,
    update_search_index,
    is_elasticsearch_backend,
)


@unittest.skipUnless(
    is_elasticsearch_backend(get_search_backend()),
    "Boost reduction is only availalbe in Elasticsearch backends",
)
@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class TestNewsSearchBoostReduction(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def create_news_page(self):
        news_page = NewsPageFactory.build(title="Hammer News")
        self.homepage.add_child(instance=news_page)
        self.news_page = Page.objects.get(pk=news_page.id)

    def create_info_page(self):
        info_page = InformationPageFactory.build(title="Hammer Info")
        self.homepage.add_child(instance=info_page)
        self.info_page = Page.objects.get(pk=info_page.id)

    @override_settings(SEARCH_BOOST_FACTOR_NEWS_PAGE=1.0)
    def test_news_before_info_when_full_boost_factor(self):
        self.create_news_page()
        self.create_info_page()
        update_search_index()

        search_results = Page.objects.search("Hammer News")

        self.assertEqual(self.news_page, list(search_results)[0])
        self.assertEqual(self.info_page, list(search_results)[1])

    @override_settings(SEARCH_BOOST_FACTOR_NEWS_PAGE=0.1)
    def test_info_before_news_despite_news_better_match_when_low_boost_factor(self):
        self.create_news_page()
        self.create_info_page()
        update_search_index()

        search_results = Page.objects.search("Hammer News")

        self.assertEqual(self.info_page, list(search_results)[0])
        self.assertEqual(self.news_page, list(search_results)[1])
