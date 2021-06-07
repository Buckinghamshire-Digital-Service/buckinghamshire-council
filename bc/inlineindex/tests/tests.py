from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from wagtail.tests.utils import WagtailTestUtils

from bc.home.models import HomePage
from bc.inlineindex.tests.fixtures import InlineIndexChildFactory, InlineIndexFactory


class TestDisplayOfInlineIndexChildPages(TestCase, WagtailTestUtils):
    def setup_homepage(self):
        self.homepage = HomePage.objects.first()
        response = self.client.get(self.homepage.url)
        self.assertEqual(response.status_code, 200)

    def setup_inline_index(self, live):
        self.inline_index = InlineIndexFactory(
            parent=self.homepage, title="The Example Index", live=live
        )

    def setup_first_index_child(self, live):
        self.first_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The First Child", live=live
        )

    def setup_second_index_child(self, live):
        self.second_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Second Child", live=live
        )

    def setUp(self):
        self.request_factory = RequestFactory()
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
        self.setup_first_index_child(live=True)

        page = self.inline_index
        request = self.request_factory.get(page.url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 2)
        self.assertIn(self.first_index_child, index)
        self.assertEqual(context["next_page"], self.first_index_child)

    def test_live_request_to_live_index_not_shows_draft_child(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=False)

        page = self.inline_index
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 1)
        self.assertNotIn(self.first_index_child, index)
        self.assertNotIn("prev_page", context)  # Not included on the index page
        self.assertEqual(context["next_page"], None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.first_index_child.title)

    @override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
    def test_draft_request_to_draft_index_success(self):
        self.setup_inline_index(live=False)
        self.login()

        response = self.client.get(
            reverse("wagtailadmin_pages:view_draft", args=(self.inline_index.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inline_index.title)

    @override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
    def test_draft_request_to_draft_index_shows_draft_child(self):
        self.setup_inline_index(live=False)
        self.setup_first_index_child(live=False)
        self.login()

        page = self.inline_index
        url = reverse("wagtailadmin_pages:view_draft", args=(page.id,))
        request = self.request_factory.get(url)
        request.is_preview = True

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 2)
        self.assertIn(self.first_index_child, index)
        self.assertNotIn("prev_page", context)  # Not included on the index page
        self.assertEqual(context["next_page"], self.first_index_child)

    def test_live_request_to_live_child_shows_live_next_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=True)
        self.second_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Second Child", live=True
        )

        page = self.first_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertIn(self.second_index_child, index)
        self.assertEqual(context["prev_page"], self.inline_index)
        self.assertEqual(context["next_page"], self.second_index_child)

    def test_live_request_to_live_child_shows_live_prev_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=True)
        self.setup_second_index_child(live=True)

        page = self.second_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertIn(self.first_index_child, index)
        self.assertEqual(context["prev_page"], self.first_index_child)
        self.assertEqual(context["next_page"], None)

    def test_live_request_to_live_child_not_shows_draft_next_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=True)
        self.setup_second_index_child(live=False)

        page = self.first_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 2)
        self.assertNotIn(self.second_index_child, index)
        self.assertEqual(context["prev_page"], self.inline_index)
        self.assertEqual(context["next_page"], None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.second_index_child.title)

    def test_live_request_to_live_child_not_shows_draft_prev_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=False)
        self.setup_second_index_child(live=True)

        page = self.second_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 2)
        self.assertNotIn(self.first_index_child, index)
        self.assertEqual(context["prev_page"], self.inline_index)
        self.assertEqual(context["next_page"], None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.first_index_child.title)

    @override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
    def test_draft_request_to_draft_child_shows_draft_next_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=False)
        self.setup_second_index_child(live=False)
        self.login()

        page = self.first_index_child
        request = self.request_factory.get(
            reverse("wagtailadmin_pages:view_draft", args=(page.id,))
        )
        request.is_preview = True

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertIn(self.second_index_child, index)
        self.assertEqual(context["prev_page"], self.inline_index)
        self.assertEqual(context["next_page"], self.second_index_child)

    @override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
    def test_draft_request_to_draft_child_shows_draft_prev_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=False)
        self.setup_second_index_child(live=False)
        self.login()

        page = self.second_index_child
        request = self.request_factory.get(
            reverse("wagtailadmin_pages:view_draft", args=(page.id,))
        )
        request.is_preview = True

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertIn(self.first_index_child, index)
        self.assertEqual(context["prev_page"], self.first_index_child)
        self.assertEqual(context["next_page"], None)

    def test_live_request_to_live_child_skips_draft_next_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=True)
        self.setup_second_index_child(live=False)
        third_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Third Child", live=True
        )

        page = self.first_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertNotIn(self.second_index_child, index)
        self.assertEqual(context["prev_page"], self.inline_index)
        self.assertEqual(context["next_page"], third_index_child)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.second_index_child.title)

    def test_live_request_to_live_child_skips_draft_prev_sibling(self):
        self.setup_inline_index(live=True)
        self.setup_first_index_child(live=True)
        self.setup_second_index_child(live=False)
        third_index_child = InlineIndexChildFactory(
            parent=self.inline_index, title="The Third Child", live=True
        )

        page = third_index_child
        url = page.url
        request = self.request_factory.get(url)
        request.is_preview = False

        context = page.get_context(request)
        index = list(context["index"])
        self.assertEqual(len(index), 3)
        self.assertNotIn(self.second_index_child, index)
        self.assertEqual(context["prev_page"], self.first_index_child)
        self.assertEqual(context["next_page"], None)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.second_index_child.title)
