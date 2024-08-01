from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.models import Page, Site

from bc.family_information.tests.fixtures import (
    CategoryPageFactory,
    SubsiteHomePageFactory,
)
from bc.images.tests.fixtures import ImageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory

from .utils import (
    delete_test_indices_from_elasticsearch,
    get_search_settings_for_test,
    update_search_index,
)


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class FISPagesIncludedTest(TestCase):
    def setUp(self):
        self.fis_homepage = SubsiteHomePageFactory()

    def test_fis_page_in_search_results(self):
        image = ImageFactory()
        hit_page = self.fis_homepage.add_child(
            instance=CategoryPageFactory.build(
                title="screwdrivers",
                banner_image=image,
            )
        )
        update_search_index()
        response = self.client.get(reverse("search") + "?query=screwdrivers")

        self.assertIn(
            Page.objects.get(pk=hit_page.pk), response.context["search_results"]
        )

    def tearDown(self):
        delete_test_indices_from_elasticsearch()


class LGPSPagesSearchTest(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.default_homepage = self.default_site.root_page
        self.lgps_homepage = SubsiteHomePageFactory(is_pensions_site=True)
        self.lgps_site = Site.objects.create(
            hostname="lgps", root_page=self.lgps_homepage, is_default_site=False
        )
        image = ImageFactory()
        self.home_page_child = self.default_homepage.add_child(
            instance=InformationPageFactory.build(title="Pensions")
        )
        self.lpgs_page_child = self.lgps_homepage.add_child(
            instance=CategoryPageFactory.build(
                title="Pensions",
                banner_image=image,
            )
        )

    def test_lgps_page_not_in_search_results(self):
        response = self.client.get(reverse("search") + "?query=Pensions")
        self.assertNotIn(
            Page.objects.get(pk=self.lpgs_page_child.pk),
            response.context["search_results"],
        )
        self.assertIn(
            Page.objects.get(pk=self.home_page_child.pk),
            response.context["search_results"],
        )

    @override_settings(WAGTAILADMIN_BASE_URL="http://lgps/")
    def test_lgps_page_in_lgps_search_results(self):
        # Set the default site to be the LGPS site so that client.get() will
        # use the LGPS site's hostname
        self.default_site.is_default_site = False
        self.default_site.save()
        self.lgps_site.is_default_site = True
        self.lgps_site.save()

        response = self.client.get(reverse("search") + "?query=Pensions")
        self.assertIn(
            Page.objects.get(pk=self.lpgs_page_child.pk),
            response.context["search_results"],
        )
        self.assertNotIn(
            Page.objects.get(pk=self.home_page_child.pk),
            response.context["search_results"],
        )
