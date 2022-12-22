from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page

from bc.family_information.tests import fixtures
from bc.images.tests.fixtures import ImageFactory


class FISPagesIncludedTest(TestCase):
    def setUp(self):
        self.fis_homepage = fixtures.SubsiteHomePageFactory()

    def test_fis_page_in_search_results(self):
        image = ImageFactory()
        hit_page = self.fis_homepage.add_child(
            instance=fixtures.CategoryPageFactory.build(
                title="screwdrivers",
                banner_image=image,
            )
        )

        response = self.client.get(reverse("search") + "?query=screwdrivers")

        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )


class LGPSPagesExcludedTest(TestCase):
    def setUp(self):
        self.fis_homepage = fixtures.SubsiteHomePageFactory()

    def test_lgps_page_not_in_search_results(self):
        image = ImageFactory()
        hit_page = self.fis_homepage.add_child(
            instance=fixtures.SubsiteHomePageFactory.build(
                title="Buckinghamshire Local Government Pension Scheme",
                listing_summary="Buckinghamshire Local Government Pension Scheme",
                hero_image=image,
                banner_image=image,
                is_pensions_site=True,
            )
        )

        response = self.client.get(reverse("search") + "?query=pension")

        self.assertNotIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )
