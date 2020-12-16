from django.test import TestCase
from django.urls import reverse

from wagtail.tests.utils import WagtailTestUtils

from bc.home.models import HomePage
from bc.inlineindex.tests.fixtures import InlineIndexFactory, InlineIndexChildFactory


class TestDisplayOfInlineIndexChildPages(TestCase, WagtailTestUtils):
    def setup_homepage(self):
        self.homepage = HomePage.objects.first()
        response = self.client.get(self.homepage.url)
        self.assertEqual(response.status_code, 200)

    def setup_inline_index(self, live):
        self.inline_index = InlineIndexFactory(
            parent=self.homepage, title="The Example Index", live=live
        )

    def setup_inline_index_child(self, live):
        self.inline_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Example Child", live=live
        )

    def setUp(self):
        self.setup_homepage()

    def test_live_request_to_live_index_success(self):
        """
        Just a sanity check.
        """
        self.setup_inline_index(live=True)

        response = self.client.get(self.inline_index.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inline_index.title)

    def test_live_request_to_draft_index_fails(self):
        """
        Just a sanity check.
        """
        self.setup_inline_index(live=False)

        response = self.client.get(self.inline_index.url)

        self.assertEqual(response.status_code, 404)

    def test_live_request_to_live_index_shows_live_child(self):
        self.setup_inline_index(live=True)
        self.setup_inline_index_child(live=True)

        response = self.client.get(self.inline_index.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inline_index.title)

    def test_live_request_to_live_index_not_shows_draft_child(self):
        self.setup_inline_index(live=True)
        self.setup_inline_index_child(live=False)

        response = self.client.get(self.inline_index.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.inline_index_child.title)

    def test_draft_request_to_draft_index_success(self):
        self.setup_inline_index(live=False)
        self.login()

        response = self.client.get(
            reverse("wagtailadmin_pages:view_draft", args=(self.inline_index.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inline_index.title)

    def test_draft_request_to_draft_index_shows_draft_child(self):
        self.setup_inline_index(live=False)
        self.setup_inline_index_child(live=False)
        self.login()

        response = self.client.get(
            reverse("wagtailadmin_pages:view_draft", args=(self.inline_index.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inline_index_child.title)

    def test_live_request_to_live_child_shows_live_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_inline_index_child(live=True)
        second_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Second Child", live=True
        )

        response = self.client.get(self.inline_index_child.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, second_index_child.title)

    def test_live_request_to_live_child_not_shows_draft_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_inline_index_child(live=True)
        second_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Second Child", live=False
        )

        response = self.client.get(self.inline_index_child.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, second_index_child.title)

    def test_draft_request_to_draft_child_shows_draft_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_inline_index_child(live=False)
        second_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Second Child", live=False
        )
        self.login()

        response = self.client.get(
            reverse("wagtailadmin_pages:view_draft", args=(self.inline_index.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, second_index_child.title)
