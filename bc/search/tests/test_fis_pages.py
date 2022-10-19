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
            instance=fixtures.CategoryTypeOnePageFactory.build(
                title="screwdrivers",
                banner_image=image,
            )
        )

        response = self.client.get(reverse("search") + "?query=screwdrivers")

        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )
