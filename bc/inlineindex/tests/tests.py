from django.test import TestCase

from bc.home.models import HomePage

from bc.inlineindex.tests.fixtures import InlineIndexFactory


class TestDisplayOfChildPages(TestCase):
    def test_previewing_draft_index_shows_draft_children(self):
        homepage = HomePage.objects.first()

        response = self.client.get(homepage.url)
        self.assertEqual(response.status_code, 200)

        inline_index = InlineIndexFactory(parent=homepage, title="The Example Index")

        response = self.client.get(inline_index.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Example Index")
