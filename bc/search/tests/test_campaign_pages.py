from django import test, urls

from wagtail.core.models import Page

from bc.campaigns.tests.fixtures import CampaignPageFactory


class CampaignPagesNotIncludedTest(test.TestCase):
    def test_campaign_page_not_in_search_results(self):
        search_word = "screwdrivers"
        campaign_page = CampaignPageFactory.create(title=search_word)

        response = self.client.get(
            urls.reverse("search") + "?query={query}".format(query=search_word)
        )

        self.assertNotIn(
            Page.objects.get(pk=campaign_page.pk), response.context["search_results"]
        )
