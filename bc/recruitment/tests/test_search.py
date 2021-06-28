from urllib.parse import unquote

from django.http import QueryDict
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.core.models import Page, Site

from bc.recruitment.constants import JOB_BOARD_CHOICES
from bc.recruitment.forms import SearchAlertSubscriptionForm
from bc.recruitment.tests.fixtures import RecruitmentHomePageFactory
from bc.recruitment.utils import get_job_search_results


class SearchViewTest(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Job site (external)
        self.homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                job_board=JOB_BOARD_CHOICES[0]
            )
        )
        self.site = Site.objects.create(
            hostname="jobs.example", port=80, root_page=self.homepage
        )

    def test_sql_injection(self):
        # This decodes to "schools\x00'||SLeeP(3)&&'1", where there's a NUL character
        # 0x00 between schools and the first inverted comma.
        query_string = unquote("category=schools%00%27||SLeeP(3)%26%26%271")
        querydict = QueryDict(query_string)
        results = get_job_search_results(querydict, self.homepage)
        try:
            results.first()  # Evaluate the search results
        except ValueError:
            # Invalid strings are silently discarded, rather than raise an exception.
            self.fail(
                "SQL injection attempt caused an exception with job search results"
            )


def SubscriptionFormTest(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Job site
        self.homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                job_board=JOB_BOARD_CHOICES[0]
            )
        )
        self.site = Site.objects.create(
            hostname="jobs.example", port=80, root_page=self.homepage
        )

    def test_subscription_form_is_in_context(self):
        response = self.client.get(self.site + reverse("search"))
        self.assertIn("job_alert_form", response.context)
        self.assertEqual(
            response.context["job_alert_form"], SearchAlertSubscriptionForm
        )

    @override_settings(ENABLE_JOBS_SEARCH_ALERT_SUBSCRIPTIONS=False)
    def test_subscription_form_can_be_disabled(self):
        response = self.client.get(self.site + reverse("search"))
        self.assertNotIn("job_alert_form", response.context)
