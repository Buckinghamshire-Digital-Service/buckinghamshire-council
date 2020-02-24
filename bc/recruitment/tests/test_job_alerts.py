import datetime
import json
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from wagtail.core.models import Page, Site

import wagtail_factories
from freezegun import freeze_time

from bc.recruitment.models import JobAlertNotificationTask

from .fixtures import (
    JobAlertSubscriptionFactory,
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)

COMMAND_MODULE_PATH = "bc.recruitment.management.commands.send_job_alerts"


class JobAlertTest(TestCase):
    def setUp(self):
        root_page = Page.objects.get(id=1)

        # For simple tests
        hero_image = wagtail_factories.ImageFactory()
        recruitment_homepage = root_page.add_child(
            instance=RecruitmentHomePageFactory.build(hero_image=hero_image)
        )
        Site.objects.create(
            hostname="example.com", port=80, root_page=recruitment_homepage
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
        JobAlertNotificationTask.objects.create(
            started=instant,
            ended=instant + datetime.timedelta(minutes=1),
            is_successful=True,
        )

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            with mock.patch(
                COMMAND_MODULE_PATH + ".Command.get_queryset"
            ) as mock_get_queryset:
                out = StringIO()
                call_command("send_job_alerts", stdout=out)

                mock_get_queryset.assert_called_once_with(instant, later)

    def test_job_notified(self):
        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        subscription = JobAlertSubscriptionFactory(
            search=json.dumps({"query": "cycling"})
        )
        with freeze_time(instant) as frozen_datetime:
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
        JobAlertSubscriptionFactory(search=json.dumps({"query": "cycling"}))
        with freeze_time(
            datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        ) as frozen_datetime:
            TalentLinkJobFactory.create(title="cycling")

            frozen_datetime.tick(delta=datetime.timedelta(days=1))
            JobAlertNotificationTask.objects.create(
                started=frozen_datetime.time_to_freeze,
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
