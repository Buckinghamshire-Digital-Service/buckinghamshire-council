from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from wagtail.core.models import Page, Site

from bc.home.tests.fixtures import HomePageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory
from bc.utils.tests.factories import SystemMessageFactory


class QueryEscapingTest(TestCase):
    """Tests that query strings displayed in templates are escaped"""

    def setUp(self):
        root_page = Page.objects.get(id=1)

        homepage = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=homepage)
        self.information_page = InformationPageFactory.build(title="foo")
        homepage.add_child(instance=self.information_page)

        site = Site.objects.create(
            hostname="www.example.com",
            port=80,
            root_page=homepage,
            is_default_site=True,
        )
        SystemMessageFactory(
            site=site,
            body_no_search_results="No results found for {searchterms}, sorry.",
        )

    def test_search_query_is_displayed_with_results(self):
        response = self.client.get(reverse("search") + "?query=foo")
        self.assertIn(
            Page.objects.get(pk=self.information_page.page_ptr_id),
            response.context["search_results"].object_list,
        )
        self.assertContains(response, "foo")

    def test_search_query_is_displayed_with_no_results(self):
        response = self.client.get(reverse("search") + "?query=bar")
        self.assertEqual(response.context["search_results"].object_list.count(), 0)
        self.assertContains(response, "bar")

    def test_search_query_escaping_with_results(self):
        response = self.client.get(reverse("search") + "?query=foo+<")
        self.assertIn(
            Page.objects.get(pk=self.information_page.page_ptr_id),
            response.context["search_results"].object_list,
        )
        self.assertContains(response, escape("foo <"))
        self.assertNotContains(response, "foo <")

    def test_search_query_escaping_with_no_results(self):
        xss_string = '<svg on onload=(alert)("XSS".domain)>'
        response = self.client.get(
            reverse("search") + "?query=" + xss_string.replace(" ", "+")
        )
        self.assertEqual(response.context["search_results"].object_list.count(), 0)
        self.assertContains(response, escape(xss_string))
        self.assertNotContains(response, xss_string)
