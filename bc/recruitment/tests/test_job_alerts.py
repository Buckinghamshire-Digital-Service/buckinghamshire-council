import datetime
import json
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.http import QueryDict
from django.test import RequestFactory, TestCase, override_settings

from wagtail.models import Page, Site

from freezegun import freeze_time

from bc.home.tests.fixtures import HomePageFactory
from bc.recruitment.constants import JOB_BOARD_CHOICES, JOB_FILTERS
from bc.recruitment.models import JobAlertNotificationTask, TalentLinkJob
from bc.recruitment.utils import get_current_search, is_recruitment_site

from .fixtures import (
    JobAlertSubscriptionFactory,
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)

COMMAND_MODULE_PATH = "bc.recruitment.management.commands.send_job_alerts"


class JobAlertTest(TestCase):
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

        # Internal job site
        self.homepage_internal = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                job_board=JOB_BOARD_CHOICES[1]
            )
        )
        self.site_internal = Site.objects.create(
            hostname="internal-jobs.example",
            port=80,
            root_page=self.homepage_internal,
        )

    def test_job_alert_token(self):
        alert = JobAlertSubscriptionFactory()
        self.assertNotEqual(
            alert.token,
            "",
            msg="Token should be automatically generated when instance is saved.",
        )

        previous_token = alert.token
        alert.search = '{"query": "Test"}'
        alert.save()
        self.assertEqual(
            alert.token,
            previous_token,
            msg="Token shouldn't change when instance is updated.",
        )

        new_alert = JobAlertSubscriptionFactory()
        self.assertNotEqual(
            new_alert.token,
            "",
            msg="Token should be automatically generated when instance is saved.",
        )
        self.assertNotEqual(
            new_alert.token, previous_token, msg="Token should be unique."
        )

    @override_settings(
        ALLOWED_HOSTS=["jobs.example", "internal-jobs.example", "main.example"]
    )
    def test_utils_is_recruitment_site(self):
        factory = RequestFactory()

        recruitment_site_request = factory.get("/", SERVER_NAME=self.site.hostname)
        self.assertEqual(Site.find_for_request(recruitment_site_request), self.site)
        self.assertTrue(is_recruitment_site(self.site))

        internal_recruitment_site_request = factory.get(
            "/", SERVER_NAME=self.site_internal.hostname
        )
        self.assertEqual(
            Site.find_for_request(internal_recruitment_site_request), self.site_internal
        )
        self.assertTrue(is_recruitment_site(self.site_internal))

        # Create a main site (not recruitment site)
        main_site_homepage = self.root_page.add_child(
            instance=HomePageFactory.build_with_fk_objs_committed()
        )
        main_site = Site.objects.create(
            hostname="main.example", port=80, root_page=main_site_homepage
        )
        main_site_request = factory.get("/", SERVER_NAME=main_site.hostname)
        self.assertEqual(Site.find_for_request(main_site_request), main_site)
        self.assertFalse(is_recruitment_site(main_site))

    @override_settings(ALLOWED_HOSTS=["has-no-site-record.example"])
    def test_utils_is_recruitment_site_when_no_match_and_no_default_site_is_set(self):
        factory = RequestFactory()

        Site.objects.all().delete()
        self.assertFalse(Site.objects.filter(is_default_site=True).exists())

        has_no_site_request = factory.get("/", SERVER_NAME="has-no-site-record.example")
        site = Site.find_for_request(has_no_site_request)
        self.assertEqual(site, None)
        self.assertFalse(is_recruitment_site(site))

    def test_utils_get_current_search(self):
        query = QueryDict("query=school")
        query_json = get_current_search(query)
        self.assertEqual(query_json, json.dumps({"query": "school"}))

        query = QueryDict()
        query_json = get_current_search(query)
        self.assertEqual(query_json, json.dumps({}))

    def test_utils_get_current_search_with_filters(self):
        for filter in JOB_FILTERS:
            query = QueryDict(filter["name"] + "=test1&" + filter["name"] + "=test2&")
            query_json = get_current_search(query)
            self.assertEqual(
                query_json, json.dumps({filter["name"]: ["test1", "test2"]})
            )

    def test_utils_get_current_search_is_sorted(self):
        for filter in JOB_FILTERS:
            querystring = "{0}={3}&{0}={1}&{0}={2}".format(
                filter["name"], "test1", "test2", "test3"
            )
            query_json = get_current_search(QueryDict(querystring))

            querystring_2 = "{0}={2}&{0}={3}&{0}={1}".format(
                filter["name"], "test1", "test2", "test3"
            )
            query_json_2 = get_current_search(QueryDict(querystring_2))

            self.assertEqual(
                query_json,
                query_json_2,
                msg="Filters should be saved in same order regardless of their sort order on the querystring.",
            )

    def test_utils_get_current_search_ignores_duplicate_filters(self):
        for filter in JOB_FILTERS:
            querystring = "{0}={1}&{0}={2}".format(filter["name"], "test1", "test2")
            query_json = get_current_search(QueryDict(querystring))

            querystring_2 = "{0}={1}&{0}={2}&{0}={1}".format(
                filter["name"], "test1", "test2"
            )
            query_json_2 = get_current_search(QueryDict(querystring_2))

            self.assertEqual(
                query_json,
                query_json_2,
                msg="Duplicate values in filters should be treated as one.",
            )

    def test_utils_get_current_search_with_rogue_param(self):
        # Test with rogue query parameters (not in JOB_FILTERS)
        query = QueryDict("query=school&rogue=ha")
        query_json = get_current_search(query)
        self.assertEqual(
            query_json,
            json.dumps({"query": "school"}),
            msg="Parameters not in JOB_FILTERS should be ignored.",
        )

    def test_times(self):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant) as frozen_datetime:
            out = StringIO()
            call_command("send_job_alerts", stdout=out)

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            out = StringIO()
            call_command("send_job_alerts", stdout=out)

        first = JobAlertNotificationTask.objects.first()
        last = JobAlertNotificationTask.objects.last()
        self.assertEqual(JobAlertNotificationTask.objects.count(), 2)
        self.assertEqual(first.started, instant)
        self.assertEqual(last.started, instant + datetime.timedelta(days=1))

    def test_queryset_search(self):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant) as frozen_datetime:
            JobAlertSubscriptionFactory()
            JobAlertNotificationTask.objects.create(
                ended=frozen_datetime.time_to_freeze + datetime.timedelta(minutes=1),
                is_successful=True,
            )

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".Command.get_queryset",
                return_value=TalentLinkJob.objects.none(),
            ) as mock_get_queryset:
                mock_get_queryset
                out = StringIO()
                call_command("send_job_alerts", stdout=out)

                mock_get_queryset.assert_called_once_with(
                    start_time=instant,
                    end_time=instant + datetime.timedelta(days=1),
                )

    def test_queryset_search_with_new_alert(self):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant) as frozen_datetime:
            JobAlertNotificationTask.objects.create(
                ended=frozen_datetime.time_to_freeze + datetime.timedelta(minutes=1),
                is_successful=True,
            )

            frozen_datetime.tick(delta=datetime.timedelta(hours=1))
            alert = JobAlertSubscriptionFactory()

            frozen_datetime.tick(delta=datetime.timedelta(hours=23))
            with mock.patch(
                COMMAND_MODULE_PATH + ".Command.get_queryset",
                return_value=TalentLinkJob.objects.none(),
            ) as mock_get_queryset:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)

                alert.refresh_from_db()
                mock_get_queryset.assert_called_once_with(
                    start_time=alert.created,
                    end_time=instant + datetime.timedelta(days=1),
                )

    def test_job_notified(self):
        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant) as frozen_datetime:
            subscription = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}), homepage=self.homepage
            )

            frozen_datetime.tick()
            TalentLinkJobFactory.create(title="cycling", homepage=self.homepage)

            frozen_datetime.tick()
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_notified_respects_job_board(self):
        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant) as frozen_datetime:
            JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}),
                homepage=self.homepage,
            )
            subscription_2 = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}),
                homepage=self.homepage_internal,
            )

            frozen_datetime.tick()
            TalentLinkJobFactory.create(
                title="cycling", homepage=self.homepage_internal
            )

            frozen_datetime.tick()
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("0 emails sent", output)
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage_internal.id}) evaluated",
                    output,
                )
                self.assertIn("1 emails sent", output)

                mock_message_class.assert_called_once_with(
                    to=[subscription_2.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_not_notified_if_a_successful_task_was_started_since_import(self):
        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            JobAlertSubscriptionFactory(search=json.dumps({"query": "cycling"}))

            frozen_datetime.tick()
            TalentLinkJobFactory.create(title="cycling")

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            JobAlertNotificationTask.objects.create(
                ended=frozen_datetime.time_to_freeze + datetime.timedelta(minutes=1),
                is_successful=True,
            )

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("0 emails sent", output)
                mock_message_class.assert_not_called()

    def test_job_is_notified_if_the_intended_earlier_task_failed(self):
        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            subscription = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}), homepage=self.homepage
            )

            frozen_datetime.tick()
            TalentLinkJobFactory.create(title="cycling", homepage=self.homepage)

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            JobAlertNotificationTask.objects.create(
                ended=frozen_datetime.time_to_freeze + datetime.timedelta(minutes=1),
                is_successful=False,
            )

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()

                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_not_notified_if_created_after_the_start_of_this_task(self):
        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant + datetime.timedelta(seconds=10)):
            # NOTE This test then travels backwards in time. 🤷
            TalentLinkJobFactory.create(title="cycling", homepage=self.homepage)

        with freeze_time(instant) as frozen_datetime:
            subscription = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}), homepage=self.homepage
            )
            frozen_datetime.tick()
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("0 emails sent", output)
                mock_message_class.assert_not_called()

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_not_notified_if_created_before_the_subscription(self):

        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            TalentLinkJobFactory.create(title="cycling", homepage=self.homepage)

            frozen_datetime.tick()
            JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"}), homepage=self.homepage
            )

            frozen_datetime.tick(delta=datetime.timedelta(hours=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn(
                    f"1 subscriptions for job site (id={self.homepage.id}) evaluated",
                    output,
                )
                self.assertIn("0 emails sent", output)
                mock_message_class.assert_not_called()
