from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.html import escape

from wagtail.models import Page, Site

import requests
from elasticsearch.exceptions import TransportError

from bc.home.tests.fixtures import HomePageFactory
from bc.recruitment.utils import is_recruitment_site
from bc.standardpages.tests.fixtures import InformationPageFactory
from bc.utils.tests.factories import SystemMessageFactory

from .utils import (
    delete_test_indices_from_elasticsearch,
    get_search_settings_for_test,
    update_search_index,
)


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
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
        update_search_index()

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

    def tearDown(self):
        delete_test_indices_from_elasticsearch()


@override_settings(SEARCH_BACKEND=get_search_settings_for_test())
class BackoffSearchTest(TestCase):
    """Tests that backoff returns"""

    def setUp(self):
        root_page = Page.objects.get(id=1)

        homepage = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=homepage)
        self.information_page = InformationPageFactory.build(title="foo")
        homepage.add_child(instance=self.information_page)

        self.site = Site.objects.create(
            hostname="www.example.com",
            port=80,
            root_page=homepage,
            is_default_site=True,
        )
        SystemMessageFactory(
            site=self.site,
            body_no_search_results="No results found for {searchterms}, sorry.",
        )
        update_search_index()

    @mock.patch("bc.search.views.is_recruitment_site")
    def test_backoff_search_applied(self, mocked_method):
        """
        This test checks that the below exceptions when raised within the view
        are caught and the backoff is applied.

        This is done by making the is_recruitment_site method to raise these errors
        to mimic the Wagtail Search backend behaviour.

        Using this method done for ease of testing and to avoid having to mock the Wagtail Search backend.
        """
        mocked_method.side_effect = [
            TransportError("Test Error"),
            requests.exceptions.ConnectionError(),
            requests.exceptions.Timeout(),
            is_recruitment_site(self.site),
        ]

        response = self.client.get(reverse("search") + "?query=foo")

        self.assertEqual(mocked_method.call_count, 4)

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        delete_test_indices_from_elasticsearch()
