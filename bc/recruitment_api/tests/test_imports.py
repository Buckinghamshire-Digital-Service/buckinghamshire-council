import datetime
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from freezegun import freeze_time

from bc.recruitment.models import JobCategory, TalentLinkJob
from bc.recruitment.tests.fixtures import JobCategoryFactory, TalentLinkJobFactory
from bc.recruitment_api.utils import update_job_from_ad

from .fixtures import get_advertisement, no_further_pages_response

# Job category title to match dummy Job Group in get_advertisement() fixture
FIXTURE_JOB_CATEGORY_TITLE = "Schools & Early Years - Support"


class ImportTestMixin:
    def get_mocked_client(self, advertisements=None):
        if advertisements is None:
            advertisements = [get_advertisement()]

        # create matching category
        JobCategoryFactory(title=FIXTURE_JOB_CATEGORY_TITLE)

        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {"advertisements": {"advertisement": advertisements}, "totalResults": 143},
            no_further_pages_response,
        ]
        return client


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class ImportTest(TestCase, ImportTestMixin):
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
        self.assertEqual(
            JobCategory.objects.filter(title=FIXTURE_JOB_CATEGORY_TITLE).count(),
            1,
            msg="Category should be inserted if --import_categories is specified.",
        )

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

        def error_or_original(job, ad, defaults, import_categories):
            """ Raise an error for id 1 only"""
            if job.talentlink_id == 1:
                raise KeyError(error_message)
            else:
                return update_job_from_ad(job, ad, defaults, import_categories)

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


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class JobCategoriesTest(TestCase, ImportTestMixin):
    def test_import_with_missing_categories(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()
        JobCategory.objects.all().delete()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)
        self.assertIn("JobCategory matching query does not exist.", output)
        self.assertEqual(
            JobCategory.objects.all().count(),
            0,
            msg="Category should not be inserted if --import_categories is not specified.",
        )

    def test_import_missing_categories(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()
        JobCategory.objects.all().delete()

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)
        self.assertEqual(
            JobCategory.objects.filter(title=FIXTURE_JOB_CATEGORY_TITLE).count(),
            1,
            msg="Category should be inserted if --import_categories is specified.",
        )

    def test_update_existing_job_with_missing_categories(self, mock_get_client):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()
        JobCategory.objects.get(title=FIXTURE_JOB_CATEGORY_TITLE).delete()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)
        self.assertIn("JobCategory matching query does not exist.", output)
        self.assertEqual(
            JobCategory.objects.filter(title=FIXTURE_JOB_CATEGORY_TITLE).count(),
            0,
            msg="Category should not be inserted if --import_categories is not specified.",
        )

    def test_update_existing_job_and_importing_missing_categories(
        self, mock_get_client
    ):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()
        JobCategory.objects.get(title=FIXTURE_JOB_CATEGORY_TITLE).delete()

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("1 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class DeletedAndUpdatedJobsTest(TestCase, ImportTestMixin):
    def test_job_number_clash_with_existing_job(self, mock_get_client):
        job_number = "FS10000"
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)

        job = TalentLinkJobFactory(
            talentlink_id=1, job_number=job_number, last_imported=instant
        )

        advertisements = [
            get_advertisement(talentlink_id=1, job_number=job_number),
            get_advertisement(talentlink_id=2, job_number=job_number),
        ]
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=mock.MagicMock())

        jobs = TalentLinkJob.objects.filter(job_number=job_number)
        self.assertEqual(jobs.count(), 2)
        # Both jobs have been (re)imported
        for job in jobs:
            self.assertEqual(job.last_imported, later)

    def test_job_number_can_be_changed(self, mock_get_client):
        old_number = "FS10000"
        new_number = "FS10001"
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)

        job = TalentLinkJobFactory(
            talentlink_id=1, job_number=old_number, last_imported=instant
        )

        advertisements = [get_advertisement(talentlink_id=1, job_number=new_number)]
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=mock.MagicMock())

        # No new job has been created
        self.assertEqual(TalentLinkJob.objects.count(), 1)
        job.refresh_from_db()

        self.assertEqual(job.talentlink_id, 1)
        self.assertEqual(job.job_number, new_number)
        # The job has been reimported
        self.assertEqual(job.last_imported, later)

    def test_job_missing_from_import(self, mock_get_client):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        job = TalentLinkJobFactory(talentlink_id=1, last_imported=instant)
        self.assertEqual(TalentLinkJob.objects.count(), 1)

        advertisements = []
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        call_command("import_jobs", stdout=mock.MagicMock())

        # No new job has been created
        self.assertEqual(TalentLinkJob.objects.count(), 1)
        job.refresh_from_db()
        # The job has not been reimported
        self.assertEqual(job.last_imported, instant)
