from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.core.models import Page
from wagtail.search.models import Query

from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory

from .utils import (
    delete_test_indices_from_elasticsearch,
    get_search_settings_for_test,
    update_search_index,
)


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class SearchPromotionsTest(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_basic_search_behaviour(self):
        hit_page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                title="screwdrivers", listing_summary="abcdef",
            )
        )
        update_search_index()

        response = self.client.get(reverse("search") + "?query=screwdrivers")
        self.assertContains(response, hit_page.listing_summary)
        self.assertEqual(len(response.context["search_results"]), 1)
        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )

    def test_search_promotions_shown(self):
        promoted_page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                title="spanners", listing_summary="ghijkl",
            )
        )
        update_search_index()
        response = self.client.get(reverse("search") + "?query=screwdrivers")
        self.assertEqual(len(response.context["search_results"]), 0)

        query = Query.objects.get(query_string="screwdrivers")
        promotion = SearchPromotion.objects.create(
            query=query, page=promoted_page, description="",
        )

        response = self.client.get(reverse("search") + "?query=screwdrivers")
        self.assertContains(response, promoted_page.listing_summary)
        self.assertEqual(len(response.context["search_results"]), 1)
        self.assertIn(promotion, response.context["search_results"])

    def test_search_promotions_included_in_total_shown(self):
        hit_page = self.homepage.add_child(
            instance=InformationPageFactory.build(title="screwdrivers",)
        )
        update_search_index()
        response = self.client.get(reverse("search") + "?query=screwdrivers")
        self.assertEqual(len(response.context["search_results"]), 1)
        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )

        promoted_page = self.homepage.add_child(
            instance=InformationPageFactory.build(title="spanners",)
        )
        update_search_index()
        query = Query.objects.get(query_string="screwdrivers")
        promotion = SearchPromotion.objects.create(
            query=query, page=promoted_page, description="",
        )

        response = self.client.get(reverse("search") + "?query=screwdrivers")
        self.assertEqual(len(response.context["search_results"]), 2)
        self.assertIn(promotion, response.context["search_results"])
        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )

    def test_search_promotions_show_custom_descriptions(self):
        promoted_page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                title="spanners", listing_summary="mnopqr",
            )
        )
        update_search_index()
        query = Query.objects.create(query_string="spanners")
        promotion = SearchPromotion.objects.create(
            query=query, page=promoted_page, description="stuvwx",
        )

        response = self.client.get(reverse("search") + "?query=spanners")
        self.assertContains(response, promotion.description)

    def test_search_promotions_default_to_usual_descriptions(self):
        promoted_page = self.homepage.add_child(
            instance=InformationPageFactory.build(
                title="spanners", listing_summary="mnopqr",
            )
        )
        update_search_index()

        query = Query.objects.create(query_string="spanners")
        SearchPromotion.objects.create(
            query=query, page=promoted_page, description="",
        )

        response = self.client.get(reverse("search") + "?query=spanners")
        self.assertContains(response, promoted_page.listing_summary)

    def test_search_promotions_not_listed_twice(self):
        hit_page = self.homepage.add_child(
            instance=InformationPageFactory.build(title="hammers",)
        )
        update_search_index()
        response = self.client.get(reverse("search") + "?query=hammers")
        self.assertEqual(len(response.context["search_results"]), 1)

        query = Query.objects.get(query_string="hammers")
        promotion = SearchPromotion.objects.create(
            query=query, page=hit_page, description="foo",
        )

        response = self.client.get(reverse("search") + "?query=hammers")
        self.assertEqual(len(response.context["search_results"]), 1)
        self.assertIn(promotion, response.context["search_results"])

    def tearDown(self):
        delete_test_indices_from_elasticsearch()
