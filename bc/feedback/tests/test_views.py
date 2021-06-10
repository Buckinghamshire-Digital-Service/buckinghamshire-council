from http import HTTPStatus

from django import test, urls

from wagtail.core import models as wagtail_models

from bc.feedback.models import FeedbackComment, UsefulnessFeedback
from bc.standardpages.tests.fixtures import InformationPageFactory


class CreateInfoPageMixin:
    def setUp(self):
        self.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)


class TestUsefulnessFeedbackCreateView(CreateInfoPageMixin, test.TestCase):
    def setUp(self):
        super().setUp()
        self.client = test.Client()
        self.url = urls.reverse("feedback:usefulness_feedback_create")

    def test_get_fails(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_post_missing_data_returns_bad_request(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_form_prefix_in_post_data_is_used(self):
        """
        Test that the form is instantiated with the posted value of 'form_prefix'
        """
        payload = {
            "form_prefix": "foo",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }

        response = self.client.post(self.url, data=payload, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Thank you for your feedback")

    def test_bad_form_prefix_in_post_data_results_in_invalid_form(self):
        payload = {
            "form_prefix": "bar",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }

        response = self.client.post(self.url, data=payload, follow=True)
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
            "form_prefix": "foo",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Thank you for your feedback")

    def test_post_creates_entry_in_db(self):
        payload = {
            "form_prefix": "foo",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }
        self.assertEqual(UsefulnessFeedback.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(UsefulnessFeedback.objects.count(), 1)
        feedback = UsefulnessFeedback.objects.last()

        with self.subTest("Page URL is denormalised"):
            self.assertEqual(feedback.original_url, feedback.page.url)

    def test_page_with_permissible_long_url(self):
        """Test that a URL longer than 200 characters can be saved."""
        self.info_page.slug = "a" * 200
        self.info_page.save()
        self.assertGreater(len(self.info_page.url), 200)
        payload = {
            "form_prefix": "foo",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }
        self.assertEqual(UsefulnessFeedback.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(UsefulnessFeedback.objects.count(), 1)
        feedback = UsefulnessFeedback.objects.last()

        with self.subTest("Page URL is saved as expected"):
            self.assertEqual(feedback.original_url, feedback.page.url)

    def test_truncation_of_urls(self):
        """Test that a URL longer than 2048 characters can be saved, but truncated."""
        parent_page = self.info_page
        for _ in range(11):
            child_page = InformationPageFactory.build(slug="a" * 200)
            parent_page.add_child(instance=child_page)
            parent_page = child_page

        self.assertGreater(len(child_page.url), 2048)
        payload = {
            "form_prefix": "foo",
            "foo-page": child_page.id,
            "foo-useful": True,
        }
        self.assertEqual(UsefulnessFeedback.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(UsefulnessFeedback.objects.count(), 1)
        feedback = UsefulnessFeedback.objects.last()

        with self.subTest("Denormalised URL is truncated"):
            self.assertNotEqual(feedback.original_url, feedback.page.url)
            self.assertTrue(feedback.page.url.startswith(feedback.original_url))
            self.assertEqual(len(feedback.original_url), 2048)


class TestFeedbackCommentCreateView(CreateInfoPageMixin, test.TestCase):
    def setUp(self):
        super().setUp()
        self.client = test.Client()
        self.url = urls.reverse("feedback:feedback_comment_create")

    def test_get_fails(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_post_valid_data(self):
        payload = {
            "comment_form-page": self.info_page.id,
            "comment_form-action": "I was trying something.",
            "comment_form-issue": "Something went wrong.",
        }
        self.assertEqual(FeedbackComment.objects.count(), 0)

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(FeedbackComment.objects.count(), 1)
        feedback_comment = FeedbackComment.objects.last()

        with self.subTest("Submission is stored"):
            self.assertEqual(feedback_comment.action, payload["comment_form-action"])
            self.assertEqual(feedback_comment.issue, payload["comment_form-issue"])
            self.assertEqual(feedback_comment.page.id, self.info_page.id)

        with self.subTest("Page URL is denormalised"):
            self.assertEqual(feedback_comment.original_url, feedback_comment.page.url)

    def test_post_empty_action(self):
        payload = {
            "comment_form-page": self.info_page.id,
            "comment_form-action": "",
            "comment_form-issue": "Something went wrong.",
        }

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("action", response.json()["form"]["errors"])

    def test_post_too_long_action(self):
        payload = {
            "comment_form-page": self.info_page.id,
            "comment_form-action": "A" * 501,
            "comment_form-issue": "Something went wrong.",
        }

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("action", response.json()["form"]["errors"])
