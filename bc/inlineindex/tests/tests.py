from django.test import TestCase

from bc.home.models import HomePage

from bc.inlineindex.tests.fixtures import InlineIndexFactory


class TestDisplayOfChildPages(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

        response = self.client.get(self.homepage.url)
        self.assertEqual(response.status_code, 200)

    def test_live_request_to_live_index_success(self):
        """
        Just a sanity check.
        """
        inline_index = InlineIndexFactory(
            parent=self.homepage, title="The Example Index"
        )

        response = self.client.get(inline_index.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Example Index")

    def test_live_request_to_draft_index_fails(self):
        """
        Just a sanity check.
        """
        inline_index = InlineIndexFactory(
            parent=self.homepage, title="The Example Index", live=False
        )

        response = self.client.get(inline_index.url)

        self.assertEqual(response.status_code, 404)

    def test_previewing_draft_index_shows_draft_children(self):
        pass
