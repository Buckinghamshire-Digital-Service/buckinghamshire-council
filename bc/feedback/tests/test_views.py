from http import HTTPStatus

from django import test, urls

from wagtail.core import models as wagtail_models

from bc.feedback.models import UsefulnessFeedback
from bc.standardpages.tests.fixtures import InformationPageFactory


class TestUsefulnessFeedbackCreateView(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = urls.reverse("feedback:create_usefulness_feedback")

        self.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page

    def create_info_page(self):
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)

        self.assertIsNotNone(self.info_page.id)

    def test_get_fails(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_post_missing_data_returns_bad_request(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_post_shows_to_thank_you_page(self):
        """
        Test that successful post redirects to thank you page.

        This will not be the typical behaviour, as the form submission is supposed to be
        handled in JS. Having the thank you page present allows for progressive
        enhancement of the feedback feature and allows users without JS to submit the
        form and have a somewhat logical behaviour.

        """
        self.create_info_page()
        payload = {
            "page": self.info_page.id,
            "useful": True,
        }

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Thank you for your feedback")

    def test_post_creates_entry_in_db(self):
        self.create_info_page()
        payload = {
            "page": self.info_page.id,
            "useful": True,
        }
        self.assertEqual(UsefulnessFeedback.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(UsefulnessFeedback.objects.count(), 1)
