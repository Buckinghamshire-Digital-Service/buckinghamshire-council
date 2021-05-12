from http import HTTPStatus

from django import test, urls

from wagtail.core import models as wagtail_models

from bc.feedback.models import FeedbackComment, UsefulnessFeedback
from bc.standardpages.tests.fixtures import InformationPageFactory


class CreateInfoPageMixin:
    @classmethod
    def setUpTestData(cls):
        cls.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        cls.root_page = cls.default_site.root_page
        cls.info_page = InformationPageFactory.build()
        cls.root_page.add_child(instance=cls.info_page)


class TestUsefulnessFeedbackCreateView(CreateInfoPageMixin, test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = urls.reverse("feedback:usefulness_feedback_create")

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
        payload = {
            "page": self.info_page.id,
            "useful": True,
        }

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Thank you for your feedback")

    def test_post_creates_entry_in_db(self):
        payload = {
            "page": self.info_page.id,
            "useful": True,
        }
        self.assertEqual(UsefulnessFeedback.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(UsefulnessFeedback.objects.count(), 1)


class TestFeedbackCommentCreateView(CreateInfoPageMixin, test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = urls.reverse("feedback:feedback_comment_create")

    def test_get_fails(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_post_valid_data(self):
        payload = {
            "page": self.info_page.id,
            "action": "I was trying something.",
            "issue": "Something went wrong.",
        }
        self.assertEqual(FeedbackComment.objects.count(), 0)

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(FeedbackComment.objects.count(), 1)
        feedback_comment = FeedbackComment.objects.last()
        self.assertEqual(feedback_comment.action, payload["action"])
        self.assertEqual(feedback_comment.issue, payload["issue"])
        self.assertEqual(feedback_comment.page.id, self.info_page.id)
