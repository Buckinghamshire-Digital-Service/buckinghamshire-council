from datetime import datetime
from http import HTTPStatus

from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse

from wagtail import models as wagtail_models
from wagtail.test.utils import WagtailTestUtils

from freezegun import freeze_time

from bc.feedback.models import FeedbackComment, UsefulnessFeedback
from bc.feedback.views import FeedbackCommentReportView, UsefulnessFeedbackReportView
from bc.home.tests.fixtures import HomePageFactory
from bc.standardpages.tests.fixtures import InformationPageFactory


class CreateInfoPageMixin:
    def setUp(self):
        self.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)


class TestUsefulnessFeedbackCreateView(CreateInfoPageMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("feedback:usefulness_feedback_create")

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

    def test_csrf_exemption(self):
        """Test that no CSRF token is required with the form"""
        payload = {
            "form_prefix": "foo",
            "foo-page": self.info_page.id,
            "foo-useful": True,
        }

        client = Client(enforce_csrf_checks=True)
        response = client.post(self.url, data=payload, follow=True)

        with self.subTest("Status code"):
            # A CSRF-requiring view would return a 403 status code if the CSRF field
            # were needed.
            self.assertEqual(response.status_code, HTTPStatus.OK)
        with self.subTest("response cookies"):
            self.assertNotIn("csrftoken", response.cookies)


class TestUsefulnessFeedbackFormTemplate(CreateInfoPageMixin, TestCase):
    """Test that we do not set a CSRF token cookie.

    There is no view associated with GET requests for the form. The form template is
    included in the base page template. Therefore we test the request for a page, not a
    view.
    """

    def _test_csrf_cookie_is_not_set(self, url):
        response = self.client.get(url)
        with self.subTest("The cookie is not in the response."):
            self.assertNotIn("csrftoken", response.cookies)
        with self.subTest("The cookie is not stored by the client."):
            self.assertNotIn("csrftoken", self.client.cookies)

    def test_csrf_cookie_is_not_set_on_info_page(self):
        self._test_csrf_cookie_is_not_set(self.info_page.url)

    def test_csrf_cookie_is_not_set_on_home_page(self):
        home_page = HomePageFactory.build_with_fk_objs_committed()
        self.root_page.add_child(instance=home_page)
        self._test_csrf_cookie_is_not_set(home_page.url)


class TestFeedbackCommentCreateView(CreateInfoPageMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("feedback:feedback_comment_create")

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

    def test_page_with_permissible_long_url(self):
        """Test that a URL longer than 200 characters can be saved."""
        self.info_page.slug = "a" * 200
        self.info_page.save()
        self.assertGreater(len(self.info_page.url), 200)
        payload = {
            "comment_form-page": self.info_page.id,
            "comment_form-action": "I was trying something.",
            "comment_form-issue": "Something went wrong.",
        }
        self.assertEqual(FeedbackComment.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(FeedbackComment.objects.count(), 1)
        feedback_comment = FeedbackComment.objects.last()

        with self.subTest("Page URL is saved as expected"):
            self.assertEqual(feedback_comment.original_url, feedback_comment.page.url)

    def test_truncation_of_urls(self):
        """Test that a URL longer than 2048 characters can be saved, but truncated."""
        parent_page = self.info_page
        for _ in range(11):
            child_page = InformationPageFactory.build(slug="a" * 200)
            parent_page.add_child(instance=child_page)
            parent_page = child_page

        self.assertGreater(len(child_page.url), 2048)
        payload = {
            # "comment_form-page": self.info_page.id,
            "comment_form-page": child_page.id,
            "comment_form-action": "I was trying something.",
            "comment_form-issue": "Something went wrong.",
        }
        self.assertEqual(FeedbackComment.objects.count(), 0)

        response = self.client.post(self.url, data=payload, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(FeedbackComment.objects.count(), 1)
        feedback_comment = FeedbackComment.objects.last()

        with self.subTest("Denormalised URL is truncated"):
            self.assertNotEqual(
                feedback_comment.original_url, feedback_comment.page.url
            )
            self.assertTrue(
                feedback_comment.page.url.startswith(feedback_comment.original_url)
            )
            self.assertEqual(len(feedback_comment.original_url), 2048)

    def test_csrf_exemption(self):
        """Test that no CSRF token is required with the form"""
        payload = {
            "comment_form-page": self.info_page.id,
            "comment_form-action": "I was trying something.",
            "comment_form-issue": "Something went wrong.",
        }
        client = Client(enforce_csrf_checks=True)
        response = client.post(self.url, data=payload)

        with self.subTest("Status code"):
            # A CSRF-requiring view would return a 403 status code if the CSRF field
            # were needed.
            self.assertEqual(response.status_code, HTTPStatus.OK)
        with self.subTest("response cookies"):
            self.assertNotIn("csrftoken", response.cookies)


class TestFeedbackFormFeatureFlags(CreateInfoPageMixin, TestCase):
    expected_strings = [
        "data-extra-feedback-block",
        "data-no-form",
        "data-yes-form",
        'id="extra-feedback-block"',
        'id="page-feedback-no"',
    ]
    expected_context_keys = [
        "yes_form",
        "no_form",
        "comment_form",
    ]

    def test_form_is_displayed(self):
        response = self.client.get(self.info_page.url)
        rendered = response.content.decode()
        for string in self.expected_strings:
            with self.subTest(string=string):
                self.assertIn(string, rendered)

        for key in self.expected_context_keys:
            with self.subTest(key=key):
                self.assertIn(key, response.context)

    @override_settings(ENABLE_FEEDBACK_WIDGET=False)
    def test_form_can_be_disabled(self):
        response = self.client.get(self.info_page.url)
        rendered = response.content.decode()
        for string in self.expected_strings:
            with self.subTest(string=string):
                self.assertNotIn(string, rendered)

        for key in self.expected_context_keys:
            with self.subTest(key=key):
                self.assertNotIn(key, response.context)


@freeze_time("2024-01-09 12:00:00")
class TestUsefulnessFeedbackReportView(WagtailTestUtils, TestCase):
    def setUp(self):
        self.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page

        # Create info pages
        self.info_page_1 = InformationPageFactory.build()
        self.info_page_2 = InformationPageFactory.build()

        # Add info pages to root page
        self.root_page.add_child(instance=self.info_page_1)
        self.root_page.add_child(instance=self.info_page_2)

        self.user = self.login()
        self.url = reverse("usefuleness_feedback_report")

        # Create some feedbacks
        self.useful_feedback = UsefulnessFeedback.objects.create(
            created=datetime.now(),
            page=self.info_page_1,
            original_url=self.info_page_1.url,
            useful=True,
        )
        self.useless_feedback = UsefulnessFeedback.objects.create(
            created=datetime.now(),
            page=self.info_page_2,
            original_url=self.info_page_2.url,
            useful=False,
        )

    def test_view_filters_have_results(self):
        factory = RequestFactory()

        # Filter for useful feedback in the expected date rangae
        request = factory.get(
            self.url,
            {
                "created_after": "2024-01-08",
                "created_before": "2024-01-10",
                "useful": True,
            },
        )

        # Set the request user
        request.user = self.user

        # Create an instance of the view
        view = UsefulnessFeedbackReportView()

        # Set the request on the view
        view.request = request

        # Get the queryset
        queryset = view.get_queryset()

        # Assert that only useful feedbacks within the specified date range are included
        self.assertEqual(list(queryset), [self.useful_feedback])

        # Filter for useless feedback in the expected date rangae
        request = factory.get(
            self.url,
            {
                "created_after": "2024-01-08",
                "created_before": "2024-01-10",
                "useful": False,
            },
        )

        # Set the request on the view
        view.request = request

        # Get the queryset
        queryset = view.get_queryset()

        # Assert that only useless feedbacks within the specified date range are included
        self.assertEqual(list(queryset), [self.useless_feedback])

    def test_view_filters_have_no_results(self):
        factory = RequestFactory()

        # Create a request with date filters without hits
        request = factory.get(
            self.url,
            {"created_after": "2024-01-10"},
        )

        # Set the request user
        request.user = self.user

        # Create an instance of the view
        view = UsefulnessFeedbackReportView()

        # Set the request on the view
        view.request = request

        # Get the queryset
        queryset = view.get_queryset()

        # Assert that there are no results
        self.assertEqual(queryset.count(), 0)


@freeze_time("2024-01-09 12:00:00")
class TestFeedbackCommentReportView(WagtailTestUtils, TestCase):
    def setUp(self):
        self.default_site = wagtail_models.Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)

        self.user = self.login()
        self.url = reverse("feedback_comment_report")

        # Create a FeedbackComment
        self.comment = FeedbackComment.objects.create(
            created=datetime.now(),
            page=self.info_page,
            action="I was doing X",
            issue="Y went wrong",
        )

    def test_view_date_filter_has_results(self):
        factory = RequestFactory()

        # Create a request with date filters with expected hits
        request = factory.get(
            self.url,
            {"created_after": "2024-01-08", "created_before": "2024-01-10"},
        )

        # Set the request user
        request.user = self.user

        # Create an instance of the view
        view = FeedbackCommentReportView()

        # Set the request on the view
        view.request = request

        # Get the queryset
        queryset = view.get_queryset()

        # Assert that only feedback comments within the specified date range are included
        self.assertEqual(list(queryset), [self.comment])

    def test_view_date_filter_has_no_results(self):
        factory = RequestFactory()

        # Create a request with date filters without hits
        request = factory.get(self.url, {"created_after": "2024-01-10"})

        # Set the request user
        request.user = self.user

        # Create an instance of the view
        view = FeedbackCommentReportView()

        # Set the request on the view
        view.request = request

        # Get the queryset
        queryset = view.get_queryset()

        # Assert that only feedback comments within the specified date range are included
        self.assertEqual(queryset.count(), 0)
