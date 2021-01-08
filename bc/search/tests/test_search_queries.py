from django.conf import settings
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.core.models import Page, Site
from wagtail.search.models import Query

from bc.home.models import HomePage
from bc.home.tests.fixtures import HomePageFactory
from bc.search.views import SearchView
from bc.standardpages.tests.fixtures import IndexPageFactory, InformationPageFactory

from .utils import (
    delete_test_indices_from_elasticsearch,
    search_backend_settings,
    update_search_index,
)

SECOND_HOSTNAME = "second.example"


@override_settings(SEARCH_BACKEND=search_backend_settings)
@override_settings(ALLOWED_HOSTS=settings.ALLOWED_HOSTS + [SECOND_HOSTNAME])
class SectionAnnotationsTest(TestCase):
    def setUp(self):
        """Test the following structure:

        - site: "www site"
            - section_one: "Gozer index"
                - zuul_page: "Zuul eggs"
                    - vinz_clortho_page: "Vinz Clortho"
                - egon_page: "Egon"
            - section_two: "Dana eggs index"
        - second_site: "second site"
            - section_bee: "bee eggs"
                - cee_page: "cee"
        """

        self.site = Site.objects.get(is_default_site=True)
        self.site.site_name = "www site"
        self.site.save()

        homepage = HomePage.objects.first()

        self.section_one = IndexPageFactory.build(title="Gozer index")
        homepage.add_child(instance=self.section_one)
        self.zuul_page = InformationPageFactory.build(title="Zuul eggs")
        self.section_one.add_child(instance=self.zuul_page)
        self.egon_page = InformationPageFactory.build(title="Egon")
        self.section_one.add_child(instance=self.egon_page)

        self.vinz_clortho_page = InformationPageFactory.build(title="vinz clortho")
        self.zuul_page.add_child(instance=self.vinz_clortho_page)

        self.section_two = IndexPageFactory.build(title="Dana eggs index")
        homepage.add_child(instance=self.section_two)

        root_page = Page.objects.get(id=1)
        homepage_two = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=homepage_two)
        self.second_site = Site.objects.create(
            root_page=homepage_two, site_name="second site", hostname=SECOND_HOSTNAME,
        )

        self.section_bee = IndexPageFactory.build(title="bee eggs")
        homepage_two.add_child(instance=self.section_bee)
        self.cee_page = InformationPageFactory.build(title="cee")
        self.section_bee.add_child(instance=self.cee_page)

        update_search_index()

    def get_results(self, query, hostname=None):
        kwargs = {}
        if hostname is not None:
            kwargs["SERVER_NAME"] = hostname
        factory = RequestFactory()
        request = factory.get(reverse("search") + "?query=" + query, **kwargs)
        response = SearchView.as_view()(request)

        return response.context_data["search_results"].object_list

    def test_section_label_is_annotated(self):
        results = self.get_results("Zuul")

        self.assertEqual(results[0], Page.objects.get(pk=self.zuul_page.pk))
        self.assertEqual(results[0].specific, self.zuul_page)
        self.assertEqual(results[0].section_label, self.section_one.title)

    def test_site_label_is_annotated_for_request_from_another_site(self):
        results = self.get_results("Zuul", hostname=self.second_site.hostname)

        self.assertEqual(results[0], Page.objects.get(pk=self.zuul_page.pk))
        self.assertEqual(results[0].specific, self.zuul_page)
        self.assertEqual(results[0].section_label, self.site.site_name)

    def test_section_label_is_not_annotated_for_section_page(self):
        results = self.get_results("Gozer")

        self.assertEqual(results[0], Page.objects.get(pk=self.section_one.pk))
        self.assertEqual(results[0].specific, self.section_one)
        self.assertEqual(results[0].section_label, None)

    def test_site_label_is_annotated_for_section_page_request_from_another_site(self):
        results = self.get_results("Gozer", hostname=self.second_site.hostname)

        self.assertEqual(results[0], Page.objects.get(pk=self.section_one.pk))
        self.assertEqual(results[0].specific, self.section_one)
        self.assertEqual(results[0].section_label, self.site.site_name)

    def test_multiple_results(self):
        results = self.get_results("eggs")
        expected_section_labels = {
            self.zuul_page.pk: "Gozer index",
            self.section_two.pk: None,
            self.section_bee.pk: "second site",
        }
        self.assertCountEqual(
            results, list(Page.objects.filter(pk__in=expected_section_labels.keys()))
        )
        for result in results:
            self.assertEqual(result.section_label, expected_section_labels[result.pk])

    def test_queries(self):
        results = self.get_results("Zuul")
        with self.assertNumQueries(1):
            for result in results:
                result
                result.section_label

    def test_search_promotions_are_annotated(self):
        promotion = SearchPromotion.objects.create(
            query=Query.get("eggs"), page=self.egon_page
        )

        results = self.get_results("eggs")

        self.assertEqual(Page.objects.filter(title__contains="eggs").count(), 3)
        self.assertEqual(len(results), 4)

        self.assertEqual(results[0], promotion)
        self.assertEqual(results[0].page, Page.objects.get(pk=self.egon_page.pk))
        self.assertEqual(results[0].page.specific, self.egon_page)
        self.assertEqual(results[0].section_label, self.section_one.title)

    def test_site_label_is_annotated_for_search_promotion_request_from_another_site(
        self,
    ):
        promotion = SearchPromotion.objects.create(
            query=Query.get("Zuul"), page=self.zuul_page
        )

        results = self.get_results("Zuul")

        self.assertEqual(Page.objects.filter(title__contains="Zuul").count(), 1)
        self.assertEqual(len(results), 1)
        results = self.get_results("Zuul", hostname=self.second_site.hostname)

        self.assertEqual(results[0], promotion)
        self.assertEqual(results[0].page, Page.objects.get(pk=self.zuul_page.pk))
        self.assertEqual(results[0].page.specific, self.zuul_page)
        self.assertEqual(results[0].section_label, self.site.site_name)

    def tearDown(self):
        delete_test_indices_from_elasticsearch()
