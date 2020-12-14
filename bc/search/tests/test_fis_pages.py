from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Page

from bc.family_information.tests import fixtures
from bc.images.tests.fixtures import ImageFactory


class FISPagesExcludedTest(TestCase):
    def setUp(self):
        self.fis_homepage = fixtures.FamilyInformationHomePageFactory()

    def test_fis_page_not_in_search_results(self):
        image = ImageFactory()
        hit_page = self.fis_homepage.add_child(
            instance=fixtures.CategoryTypeOnePageFactory.build(
                title="screwdrivers", banner_image=image,
            )
        )

        response = self.client.get(reverse("search") + "?query=screwdrivers")

        self.assertNotIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )
