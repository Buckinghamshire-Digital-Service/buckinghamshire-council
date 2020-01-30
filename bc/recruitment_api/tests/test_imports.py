import datetime
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from freezegun import freeze_time

from bc.recruitment.models import TalentLinkJob
from bc.recruitment.tests.fixtures import TalentLinkJobFactory
from bc.recruitment_api.utils import update_job_from_ad

from .fixtures import get_advertisement, no_further_pages_response


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class ImportTest(TestCase):
    def get_mocked_client(self, advertisements=None):
        advertisements = advertisements or [get_advertisement()]
        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {"advertisements": {"advertisement": advertisements}, "totalResults": 143},
            no_further_pages_response,
        ]
        return client

    def test_with_mocked_client(self, mock_get_client):

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)

    def test_with_existing_job(self, mock_get_client):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("1 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)

    def test_new_job_created_date(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()

        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant):
            call_command("import_jobs", stdout=mock.MagicMock())

        job = TalentLinkJob.objects.get(talentlink_id=164579)
        self.assertEqual(job.created, instant)

    def test_existing_job_created_date(self, mock_get_client):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant):
            job = TalentLinkJobFactory(talentlink_id=164579)

        self.assertEqual(job.created, instant)

        mock_get_client.return_value = self.get_mocked_client()

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=mock.MagicMock())

        job.refresh_from_db()
        self.assertEqual(job.created, instant)

    def test_new_job_imported_date(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()

        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant):
            call_command("import_jobs", stdout=mock.MagicMock())

        job = TalentLinkJob.objects.get(talentlink_id=164579)
        self.assertEqual(job.last_imported, instant)

    def test_existing_job_imported_date(self, mock_get_client):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        job = TalentLinkJobFactory(talentlink_id=164579, last_imported=instant)

        self.assertEqual(job.last_imported, instant)

        mock_get_client.return_value = self.get_mocked_client()

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=mock.MagicMock())

        job.refresh_from_db()
        self.assertEqual(job.last_imported, later)

    @mock.patch("bc.recruitment_api.management.commands.import_jobs.update_job_from_ad")
    def test_errors_are_reported(self, mock_update_fn, mock_get_client):
        error_message = "This is a test error message"
        mock_update_fn.side_effect = KeyError(error_message)

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn(error_message, output)

    @mock.patch("bc.recruitment_api.management.commands.import_jobs.update_job_from_ad")
    def test_error_cases_are_not_imported(self, mock_update_fn, mock_get_client):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        job_1 = TalentLinkJobFactory(
            talentlink_id=1, title="Original title 1", last_imported=instant
        )
        job_2 = TalentLinkJobFactory(
            talentlink_id=2, title="Original title 2", last_imported=instant
        )

        error_message = "This is a test error message"

        def error_or_original(job, ad, defaults):
            """ Raise an error for id 1 only"""
            if job.talentlink_id == 1:
                raise KeyError(error_message)
            else:
                return update_job_from_ad(job, ad, defaults)

        mock_update_fn.side_effect = error_or_original

        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        out = StringIO()
        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn(error_message, output)
        self.assertIn("1 existing jobs updated", output)
        self.assertIn("1 errors", output)

        job_1.refresh_from_db()
        self.assertEqual(job_1.title, "Original title 1")  # not updated
        self.assertEqual(job_1.last_imported, instant)  # not updated
        job_2.refresh_from_db()
        self.assertEqual(job_2.title, "New title 2")  # job 2 has been updated
        self.assertEqual(job_2.last_imported, later)  # job 2 has been updated
