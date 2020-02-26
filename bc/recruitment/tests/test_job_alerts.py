import datetime
import json
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import RequestFactory, TestCase

from wagtail.core.models import Page, Site

import wagtail_factories
from freezegun import freeze_time

from bc.home.tests.fixtures import HomePageFactory
from bc.recruitment.models import JobAlertNotificationTask, TalentLinkJob
from bc.recruitment.utils import is_recruitment_site

from .fixtures import (
    JobAlertSubscriptionFactory,
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)

COMMAND_MODULE_PATH = "bc.recruitment.management.commands.send_job_alerts"


class JobAlertTest(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # For simple tests
        hero_image = wagtail_factories.ImageFactory()
        recruitment_homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build(hero_image=hero_image)
        )
        self.site = Site.objects.create(
            hostname="example.com", port=80, root_page=recruitment_homepage
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

    def test_utils_is_recruitment_site(self):
        request = RequestFactory().request()
        request.site = self.site
        self.assertTrue(is_recruitment_site(request))

        # Create a main site (not recruitment site)
        hero_image = wagtail_factories.ImageFactory()
        main_site_homepage = self.root_page.add_child(
            instance=HomePageFactory.build(hero_image=hero_image)
        )
        main_site = Site.objects.create(
            hostname="main.com", port=80, root_page=main_site_homepage
        )
        main_site_request = RequestFactory().request()
        main_site_request.site = main_site
        self.assertFalse(is_recruitment_site(main_site_request))

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
                    start_time=instant, end_time=instant + datetime.timedelta(days=1)
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
                search=json.dumps({"query": "cycling"})
            )

            frozen_datetime.tick()
            TalentLinkJobFactory.create(title="cycling")

            frozen_datetime.tick()
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn("1 subscriptions evaluated", output)
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
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
                self.assertIn("1 subscriptions evaluated", output)
                self.assertIn("0 emails sent", output)
                mock_message_class.assert_not_called()

    def test_job_is_notified_if_the_intended_earlier_task_failed(self):
        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            subscription = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"})
            )

            frozen_datetime.tick()
            TalentLinkJobFactory.create(title="cycling")

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
                self.assertIn("1 subscriptions evaluated", output)
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_not_notified_if_created_after_the_start_of_this_task(self):
        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant + datetime.timedelta(seconds=10)):
            # NOTE This test then travels backwards in time. 🤷
            TalentLinkJobFactory.create(title="cycling")

        with freeze_time(instant) as frozen_datetime:
            subscription = JobAlertSubscriptionFactory(
                search=json.dumps({"query": "cycling"})
            )
            frozen_datetime.tick()
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn("1 subscriptions evaluated", output)
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
                self.assertIn("1 subscriptions evaluated", output)
                self.assertIn("1 emails sent", output)
                mock_message_class.assert_called_once_with(
                    to=[subscription.email], subject=mock.ANY, body=mock.ANY
                )

    def test_job_not_notified_if_created_before_the_subscription(self):

        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            TalentLinkJobFactory.create(title="cycling")

            frozen_datetime.tick()
            JobAlertSubscriptionFactory(search=json.dumps({"query": "cycling"}))

            frozen_datetime.tick(delta=datetime.timedelta(hours=1))
            with mock.patch(
                COMMAND_MODULE_PATH + ".NotifyEmailMessage"
            ) as mock_message_class:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)
                out.seek(0)
                output = out.read()
                self.assertIn("1 subscriptions evaluated", output)
                self.assertIn("0 emails sent", output)
                mock_message_class.assert_not_called()
