from django import test, urls
from django.test import override_settings

from wagtail.models import Page

from bc.campaigns.tests.fixtures import CampaignPageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory

from .utils import (
    delete_test_indices_from_elasticsearch,
    get_search_settings_for_test,
    update_search_index,
)


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class CampaignPagesNotIncludedTest(test.TestCase):
    def test_campaign_page_not_in_search_results(self):
        search_word = "screwdrivers"
        campaign_page = CampaignPageFactory.create(title=search_word)
        update_search_index()

        response = self.client.get(
            urls.reverse("search") + "?query={query}".format(query=search_word)
        )

        self.assertNotIn(
            Page.objects.get(pk=campaign_page.pk), response.context["search_results"]
        )

    def test_campaign_page_not_in_search_result_but_info_with_same_title_is(self):
        """Sanity check."""
        search_word = "screwdrivers"
        campaign_page = CampaignPageFactory.create(title=search_word)
        information_page = InformationPageFactory.create(title=search_word)

        update_search_index()

        response = self.client.get(
            urls.reverse("search") + "?query={query}".format(query=search_word)
        )

        self.assertNotIn(
            Page.objects.get(pk=campaign_page.pk), response.context["search_results"]
        )
        self.assertIn(
            Page.objects.get(pk=information_page.pk), response.context["search_results"]
        )

    def tearDown(self):
        delete_test_indices_from_elasticsearch()
