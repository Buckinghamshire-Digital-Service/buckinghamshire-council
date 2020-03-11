import datetime
import textwrap
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from bc.recruitment.models import JobSubcategory, TalentLinkJob
from bc.recruitment.tests.fixtures import JobSubcategoryFactory, TalentLinkJobFactory
from bc.recruitment_api.utils import update_job_from_ad

from .fixtures import get_advertisement, no_further_pages_response

# Job category title to match dummy Job Group in get_advertisement() fixture
FIXTURE_JOB_SUBCATEGORY_TITLE = "Schools & Early Years - Support"


class ImportTestMixin:
    def get_mocked_client(self, advertisements=None):
        if advertisements is None:
            advertisements = [get_advertisement()]

        # create matching category
        JobSubcategoryFactory(title=FIXTURE_JOB_SUBCATEGORY_TITLE)

        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {"advertisements": {"advertisement": advertisements}, "totalResults": 143},
            no_further_pages_response,
        ]
        # TODO: add dummy content for attachments
        # Should return list of files with 'content', 'description', 'fileName', 'id', 'mimeType'
        client.service.getAttachments.side_effect = [{}]
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
            JobSubcategory.objects.filter(title=FIXTURE_JOB_SUBCATEGORY_TITLE).count(),
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
class JobSubcategoriesTest(TestCase, ImportTestMixin):
    def test_import_with_missing_subcategories(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()
        JobSubcategory.objects.all().delete()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)
        self.assertIn("JobSubcategory matching query does not exist.", output)
        self.assertEqual(
            JobSubcategory.objects.all().count(),
            0,
            msg="Subcategory should not be inserted if --import_categories is not specified.",
        )

    def test_import_missing_subcategories(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client()
        JobSubcategory.objects.all().delete()

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)
        self.assertEqual(
            JobSubcategory.objects.filter(title=FIXTURE_JOB_SUBCATEGORY_TITLE).count(),
            1,
            msg="Subcategory should be inserted if --import_categories is specified.",
        )

    def test_update_existing_job_with_missing_subcategories(self, mock_get_client):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()
        JobSubcategory.objects.get(title=FIXTURE_JOB_SUBCATEGORY_TITLE).delete()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)
        self.assertIn("JobSubcategory matching query does not exist.", output)
        self.assertEqual(
            JobSubcategory.objects.filter(title=FIXTURE_JOB_SUBCATEGORY_TITLE).count(),
            0,
            msg="Subcategory should not be inserted if --import_categories is not specified.",
        )

    def test_update_existing_job_and_importing_missing_subcategories(
        self, mock_get_client
    ):
        TalentLinkJobFactory(talentlink_id=164579)

        mock_get_client.return_value = self.get_mocked_client()
        JobSubcategory.objects.get(title=FIXTURE_JOB_SUBCATEGORY_TITLE).delete()

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


class DescriptionsTest(TestCase):
    def setUp(self):
        # create matching category
        JobSubcategoryFactory(title=FIXTURE_JOB_SUBCATEGORY_TITLE)

    def compare_processed_record(self, description, expected):

        try:
            job = TalentLinkJob.objects.get(talentlink_id=1)
        except TalentLinkJob.DoesNotExist:
            job = TalentLinkJob(talentlink_id=1)

        job = update_job_from_ad(
            job,
            get_advertisement(talentlink_id=1, description=description),
            defaults={"last_imported": timezone.now()},
        )

        expected = textwrap.dedent(expected).strip()
        self.assertEqual(job.description, expected)

    def test_basic_case(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": "<p>This is a paragraph of text.</p>",
            },
            {
                "label": "Second section",
                "order": 2,
                "value": "<p>This is a second paragraph.</p>",
            },
        ]

        expected = """
            <h3>First section</h3>
            <p>This is a paragraph of text.</p>
            <h3>Second section</h3>
            <p>This is a second paragraph.</p>
            """

        self.compare_processed_record(description, expected)

    def test_descriptions_are_updated(self):
        job = TalentLinkJobFactory(talentlink_id=1, description="Old value")
        description = [
            {
                "label": "New Info",
                "order": 1,
                "value": "<p>This is a paragraph of text.</p>",
            }
        ]
        expected = """
            <h3>New Info</h3>
            <p>This is a paragraph of text.</p>
            """
        self.assertEqual(job.description, "Old value")
        self.compare_processed_record(description, expected)

    def test_style_attributes_are_stripped(self):
        description = [
            {
                "label": "Colourful text",
                "order": 1,
                "value": '<p style="color: #2a2a2a;">This is a paragraph of text.</p>',
            }
        ]
        expected = """
            <h3>Colourful text</h3>
            <p>This is a paragraph of text.</p>
            """
        self.compare_processed_record(description, expected)

    def test_class_attributes_are_stripped(self):
        description = [
            {
                "label": "Classy text",
                "order": 1,
                "value": '<p class="manatee">This is a paragraph of text.</p>',
            }
        ]
        expected = """
            <h3>Classy text</h3>
            <p>This is a paragraph of text.</p>
            """
        self.compare_processed_record(description, expected)

    def test_ids_are_stripped(self):
        description = [
            {
                "label": "Mighty fine text",
                "order": 1,
                "value": '<p id="mediocre">This is a paragraph of text.</p>',
            }
        ]
        expected = """
            <h3>Mighty fine text</h3>
            <p>This is a paragraph of text.</p>
            """
        self.compare_processed_record(description, expected)

    def test_link_references_are_passed(self):
        description = [
            {
                "label": "Hyperlinked text",
                "order": 1,
                "value": '<p>Visit <a href="https://www.example.com">example.com</a>.\n'
                'Email <a href="mailto:user@example.org">a named user</a> for more info.</p>',
            }
        ]
        expected = """
            <h3>Hyperlinked text</h3>
            <p>Visit <a href="https://www.example.com">example.com</a>.
            Email <a href="mailto:user@example.org">a named user</a> for more info.</p>
            """
        self.compare_processed_record(description, expected)

    def test_ordering(self):
        description = [
            {
                "label": "Second section",
                "order": 2,
                "value": "<p>This is a second paragraph.</p>",
            },
            {
                "label": "First section",
                "order": 1,
                "value": "<p>This is a paragraph of text.</p>",
            },
        ]

        expected = """
            <h3>First section</h3>
            <p>This is a paragraph of text.</p>
            <h3>Second section</h3>
            <p>This is a second paragraph.</p>
            """

        self.compare_processed_record(description, expected)


class ShortDescriptionsTest(TestCase, ImportTestMixin):
    def setUp(self):
        # create matching category
        JobSubcategoryFactory(title=FIXTURE_JOB_SUBCATEGORY_TITLE)

    def compare_processed_record(self, description, expected):

        try:
            job = TalentLinkJob.objects.get(talentlink_id=1)
        except TalentLinkJob.DoesNotExist:
            job = TalentLinkJob(talentlink_id=1)

        job = update_job_from_ad(
            job,
            get_advertisement(talentlink_id=1, description=description),
            defaults={"last_imported": timezone.now()},
        )

        expected = textwrap.dedent(expected).strip()
        self.assertEqual(job.short_description, expected)

    def test_basic_case(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": "<p>This is a paragraph of text.</p>",
            },
            {
                "label": "Second section",
                "order": 2,
                "value": "<p>This is a second paragraph.</p>",
            },
        ]

        expected = "This is a paragraph of text."

        self.compare_processed_record(description, expected)

    def test_paragraph_is_first_by_order_attribute(self):
        description = [
            {
                "label": "First section",
                "order": 2,
                "value": "<p>This is a paragraph of text.</p>",
            },
            {
                "label": "Second section",
                "order": 1,
                "value": "<p>This was the second indexed, but first by order attribute.</p>",
            },
        ]

        expected = "This was the second indexed, but first by order attribute."

        self.compare_processed_record(description, expected)

    def test_all_tags_within_paragraph_are_stripped(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": """
                    <p>This <b>beefy</b> <em>emphatic</em> <strong>strong</strong>
                    <i>Italian</i> <span class="sentiment">sentiment</span> needeth not
                    <a href="https://en.wiktionary.org/wiki/koe">decoration</a>.</p>
                """,
            }
        ]

        expected = (
            "This beefy emphatic strong Italian sentiment needeth not decoration."
        )

        self.compare_processed_record(description, expected)

    def test_preceding_non_paragraph_elements_are_ignored(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": """
                    <div><h2>To be ignored</h2></div>
                    <p>To be the short description.</p>
                """,
            }
        ]

        expected = "To be the short description."

        self.compare_processed_record(description, expected)

    def test_subsequent_paragraphs_are_ignored(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": """
                    <p>Only this should be the short description.</p>
                    <p>This should be ignored.</p>
                """,
            }
        ]

        expected = "Only this should be the short description."

        self.compare_processed_record(description, expected)

    def test_plaintext_is_imported(self):
        description = [
            {"label": "First section", "order": 1, "value": "This is plaintext."}
        ]

        expected = "This is plaintext."

        self.compare_processed_record(description, expected)

    def test_html_hiding_in_plaintext_is_still_cleaned(self):
        description = [
            {
                "label": "First section",
                "order": 1,
                "value": "<div><h3>This <em>was not</em> plaintext.</h3></div>",
            }
        ]

        expected = "This was not plaintext."

        self.compare_processed_record(description, expected)


class ApplicationURLTest(TestCase, ImportTestMixin):
    def setUp(self):
        # create matching category
        JobSubcategoryFactory(title=FIXTURE_JOB_SUBCATEGORY_TITLE)

    def compare_processed_record(self, imported, expected):

        try:
            job = TalentLinkJob.objects.get(talentlink_id=1)
        except TalentLinkJob.DoesNotExist:
            job = TalentLinkJob(talentlink_id=1)

        job = update_job_from_ad(
            job,
            get_advertisement(talentlink_id=1, application_url=imported),
            defaults={"last_imported": timezone.now()},
        )

        self.assertEqual(job.application_url_query, expected)

    def test_empty_url_query(self):
        imported = ""
        expected = ""

        self.compare_processed_record(imported, expected)

    def test_basic_url_query(self):
        imported = "https://www.example.com/?spam=eggs"
        expected = "spam=eggs"

        self.compare_processed_record(imported, expected)

    def test_url_with_no_query(self):
        imported = "https://www.example.com/?"
        expected = ""

        self.compare_processed_record(imported, expected)

    def test_multi_value_dict(self):
        imported = "https://www.example.com/?spam=1&spam=2"
        expected = "spam=1&spam=2"

        self.compare_processed_record(imported, expected)


# TODO: Add tests
class AttachmentsTest(TestCase, ImportTestMixin):
    def test_attachment_is_imported(self):
        pass

    def text_job_with_no_attachment(self):
        pass

    def test_multiple_attachments_are_imported(self):
        pass

    def test_previously_imported_attachments_are_skipped(self):
        pass
