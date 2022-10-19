import factory
import wagtail_factories

from bc.campaigns.models import CampaignPage


class CampaignPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = CampaignPage

    intro = "Some intro text."
    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    listing_summary = "Campaign Page"
