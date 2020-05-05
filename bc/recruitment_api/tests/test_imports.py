import datetime
import textwrap
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from wagtail.core.models import Page

from freezegun import freeze_time

from bc.documents.models import CustomDocument
from bc.documents.tests.fixtures import DocumentFactory
from bc.images.models import CustomImage
from bc.images.tests.fixtures import ImageFactory, mock_import_image_from_url
from bc.recruitment.constants import JOB_BOARD_CHOICES
from bc.recruitment.models import JobSubcategory, TalentLinkJob
from bc.recruitment.tests.fixtures import (
    JobSubcategoryFactory,
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)
from bc.recruitment_api.utils import update_job_from_ad

from .fixtures import (
    get_advertisement,
    get_attachment,
    get_logo,
    no_further_pages_response,
)

# Job category title to match dummy Job Group in get_advertisement() fixture
FIXTURE_JOB_SUBCATEGORY_TITLE = "Schools & Early Years - Support"


class ImportTestMixin:
    def setUpRecruitmentHomePage(self):
        self.root_page = Page.objects.get(id=1)
        self.homepage = RecruitmentHomePageFactory.build_with_fk_objs_committed()
        self.root_page.add_child(instance=self.homepage)

    def get_mocked_client(
        self, advertisements=None, attachments=None, logos=None, category_titles=None
    ):
        if advertisements is None:
            advertisements = [get_advertisement()]

        if category_titles is None:
            category_titles = [FIXTURE_JOB_SUBCATEGORY_TITLE]

        for title in category_titles:
            # create matching category
            JobSubcategoryFactory(title=title)

        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {"advertisements": {"advertisement": advertisements}, "totalResults": 143},
            no_further_pages_response,
        ]

        # Attachments
        if attachments is None:
            # Add empty getAttachments response for each advertisement
            client.service.getAttachments.side_effect = [
                dict() for _ in range(len(advertisements))
            ]
        else:
            client.service.getAttachments.side_effect = attachments

        # Logos
        if logos is None:
            # Add empty getAdvertisementImages response for each advertisement
            client.service.getAdvertisementImages.side_effect = [
                dict() for _ in range(len(advertisements))
            ]
        else:
            client.service.getAdvertisementImages.side_effect = logos

        return client


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class ImportTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)

    def test_with_mocked_client(self, mock_get_client):

        mock_get_client.return_value = self.get_mocked_client()

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)

    def test_with_existing_job(self, mock_get_client):
        TalentLinkJobFactory(talentlink_id=164579, homepage=self.homepage)

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
            job = TalentLinkJobFactory(talentlink_id=164579, homepage=self.homepage)

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
        job = TalentLinkJobFactory(
            talentlink_id=164579, last_imported=instant, homepage=self.homepage
        )

        self.assertEqual(job.last_imported, instant)

        mock_get_client.return_value = self.get_mocked_client()

        later = instant + datetime.timedelta(days=1)
        with freeze_time(later):
            call_command("import_jobs", stdout=mock.MagicMock())

        job.refresh_from_db()
        self.assertEqual(job.last_imported, later)

    def test_new_job_imported_location(self, mock_get_client):
        advertisements = [
            get_advertisement(talentlink_id=1),
        ]
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant):
            call_command("import_jobs", stdout=mock.MagicMock())

        job = TalentLinkJob.objects.get(talentlink_id=1)
        self.assertEqual(job.location, "Aylesbury Vale")

        # test new location updates existing job
        new_location = "South Bucks"
        job = update_job_from_ad(
            job,
            get_advertisement(talentlink_id=1, location=new_location),
            homepage=self.homepage,
        )

        self.assertEqual(job.location, new_location)

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
        TalentLinkJobFactory(
            talentlink_id=1,
            title="Original title 1",
            last_imported=instant,
            homepage=self.homepage,
        )
        job_2 = TalentLinkJobFactory(
            talentlink_id=2,
            title="Original title 2",
            last_imported=instant,
            homepage=self.homepage,
        )
        self.assertEqual(TalentLinkJob.objects.count(), 2)

        error_message = "This is a test error message"

        def error_or_original(job, ad, homepage, defaults, import_categories):
            """ Raise an error for id 1 only"""
            if job.talentlink_id == 1:
                raise KeyError(error_message)
            else:
                return update_job_from_ad(
                    job, ad, self.homepage, defaults, import_categories
                )

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

        # job_1 should have been deleted from db as it isn't imported
        self.assertEqual(
            TalentLinkJob.objects.filter(talentlink_id=1).count(),
            0,
            msg="Jobs not in import should be deleted.",
        )

        job_2.refresh_from_db()
        self.assertEqual(job_2.title, "New title 2")  # job 2 has been updated
        self.assertEqual(job_2.last_imported, later)  # job 2 has been updated


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class JobSubcategoriesTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)

    def test_import_with_missing_subcategories(self, mock_get_client):
        mock_get_client.return_value = self.get_mocked_client(category_titles=[])

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
        mock_get_client.return_value = self.get_mocked_client(category_titles=[])

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
        TalentLinkJobFactory(talentlink_id=164579, homepage=self.homepage)

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
        TalentLinkJobFactory(talentlink_id=164579, homepage=self.homepage)

        mock_get_client.return_value = self.get_mocked_client()
        JobSubcategory.objects.get(title=FIXTURE_JOB_SUBCATEGORY_TITLE).delete()

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("1 existing jobs updated", output)
        self.assertIn("0 new jobs created", output)

    def test_case_subcategory_matching_is_case_insensitive_with_existing_categories(
        self, mock_get_client
    ):
        JobSubcategoryFactory(title="Test")
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1", job_group="tESt")
        ]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, category_titles=[]
        )

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)
        self.assertEqual(
            JobSubcategory.objects.all().count(),
            1,
            msg="JobSubcategory matching should be case insensitive",
        )
        self.assertEqual(JobSubcategory.objects.first().title, "Test")

    def test_case_subcategory_matching_is_case_insensitive_when_adding_categories(
        self, mock_get_client
    ):
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1", job_group="Test"),
            get_advertisement(talentlink_id=2, title="New title 2", job_group="tESt"),
        ]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, category_titles=[]
        )

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("2 new jobs created", output)
        self.assertEqual(
            JobSubcategory.objects.all().count(),
            1,
            msg="JobSubcategory matching should be case insensitive",
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).subcategory,
            TalentLinkJob.objects.get(talentlink_id=2).subcategory,
        )

    def test_case_subcategory_matching_is_space_insensitive_with_existing_categories(
        self, mock_get_client
    ):
        JobSubcategoryFactory(title="My Spacey Cat")
        advertisements = [
            get_advertisement(
                talentlink_id=1, title="New title 1", job_group=" my spacey   cat "
            )
        ]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, category_titles=[]
        )

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("1 new jobs created", output)
        self.assertEqual(
            JobSubcategory.objects.all().count(),
            1,
            msg="JobSubcategory matching should be case insensitive",
        )
        self.assertEqual(JobSubcategory.objects.first().title, "My Spacey Cat")

    def test_case_subcategory_matching_is_space_insensitive_when_adding_categories(
        self, mock_get_client
    ):
        advertisements = [
            get_advertisement(
                talentlink_id=1, title="New title 1", job_group=" my spacey   cat "
            ),
            get_advertisement(
                talentlink_id=2, title="New title 2", job_group="   my   spacey cat"
            ),
        ]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, category_titles=[]
        )

        out = StringIO()
        call_command("import_jobs", "--import_categories", stdout=out)
        out.seek(0)
        output = out.read()
        self.assertIn("0 existing jobs updated", output)
        self.assertIn("2 new jobs created", output)
        self.assertEqual(
            JobSubcategory.objects.all().count(),
            1,
            msg="JobSubcategory matching should be case insensitive",
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).subcategory,
            TalentLinkJob.objects.get(talentlink_id=2).subcategory,
        )


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class DeletedAndUpdatedJobsTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)

    def test_job_number_clash_with_existing_job(self, mock_get_client):
        job_number = "FS10000"
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)

        job = TalentLinkJobFactory(
            talentlink_id=1,
            job_number=job_number,
            last_imported=instant,
            homepage=self.homepage,
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
            talentlink_id=1,
            job_number=old_number,
            last_imported=instant,
            homepage=self.homepage,
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

    def test_job_missing_from_import_are_deleted(self, mock_get_client):
        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        TalentLinkJobFactory(
            talentlink_id=1, last_imported=instant, homepage=self.homepage
        )
        TalentLinkJobFactory(
            talentlink_id=2, last_imported=instant, homepage=self.homepage
        )
        self.assertEqual(TalentLinkJob.objects.count(), 2)

        advertisements = [get_advertisement(talentlink_id=2)]
        mock_get_client.return_value = self.get_mocked_client(advertisements)

        call_command("import_jobs", stdout=mock.MagicMock())

        # Only one new job remains. Jobs not in import are deleted.
        self.assertEqual(TalentLinkJob.objects.count(), 1)
        self.assertEqual(TalentLinkJob.objects.filter(talentlink_id=1).count(), 0)
        self.assertEqual(TalentLinkJob.objects.filter(talentlink_id=2).count(), 1)

    def test_job_missing_from_import_are_deleted_only_if_from_same_board(
        self, mock_get_client
    ):
        homepage_internal = RecruitmentHomePageFactory.build_with_fk_objs_committed(
            job_board=JOB_BOARD_CHOICES[1]
        )
        self.root_page.add_child(instance=homepage_internal)

        instant = datetime.datetime(2020, 1, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        TalentLinkJobFactory(
            talentlink_id=1,
            job_number="AABBSAME",
            homepage=self.homepage,
            last_imported=instant,
        )
        TalentLinkJobFactory(
            talentlink_id=2,
            job_number="CCDD",
            homepage=self.homepage,
            last_imported=instant,
        )
        TalentLinkJobFactory(
            talentlink_id=3,
            job_number="AABBSAME",
            homepage=homepage_internal,
            last_imported=instant,
        )
        self.assertEqual(
            TalentLinkJob.objects.filter(homepage=self.homepage).count(), 2
        )
        self.assertEqual(
            TalentLinkJob.objects.filter(homepage=homepage_internal).count(), 1
        )

        # Create mock client faking results for 2 boards
        board_external_advertisements = [
            get_advertisement(talentlink_id=1, job_number="AABBSAME"),
        ]
        board_internal_advertisements = [
            get_advertisement(talentlink_id=3, job_number="AABBSAME"),
        ]
        client = mock.Mock()
        client.service.getAdvertisementsByPage.side_effect = [
            {
                "advertisements": {"advertisement": board_external_advertisements},
                "totalResults": 143,
            },
            no_further_pages_response,
            {
                "advertisements": {"advertisement": board_internal_advertisements},
                "totalResults": 143,
            },
            no_further_pages_response,
        ]
        mock_get_client.return_value = client

        call_command("import_jobs", import_categories=True, stdout=mock.MagicMock())

        # Only one new job remains. Jobs not in import are deleted.
        self.assertEqual(
            TalentLinkJob.objects.filter(homepage=self.homepage).count(), 1
        )
        self.assertEqual(
            TalentLinkJob.objects.filter(homepage=homepage_internal).count(), 1
        )


class DescriptionsTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)
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
            homepage=self.homepage,
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
        job = TalentLinkJobFactory(
            talentlink_id=1, description="Old value", homepage=self.homepage
        )
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
        ImportTestMixin.setUpRecruitmentHomePage(self)
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
            homepage=self.homepage,
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
        ImportTestMixin.setUpRecruitmentHomePage(self)

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
            homepage=self.homepage,
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


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
class AttachmentsTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)

    def test_attachment_is_imported(self, mock_get_client):
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]

        job_1_get_attachments_response = [get_attachment(id=111)]

        job_2_get_attachments_response = [get_attachment(id=222)]

        attachments = [job_1_get_attachments_response, job_2_get_attachments_response]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, attachments
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 new jobs created", output)
        self.assertIn("2 new documents imported", output)

        job_1 = TalentLinkJob.objects.get(talentlink_id=1)
        job_2 = TalentLinkJob.objects.get(talentlink_id=2)

        self.assertEqual(job_1.attachments.all().count(), 1)
        self.assertEqual(job_2.attachments.all().count(), 1)
        self.assertEqual(job_1.attachments.first().talentlink_attachment_id, 111)
        self.assertEqual(job_2.attachments.first().talentlink_attachment_id, 222)

    def test_duplicate_attachment_is_not_imported(self, mock_get_client):
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]

        job_1_get_attachments_response = [get_attachment(id=111)]

        job_2_get_attachments_response = [get_attachment(id=111)]

        attachments = [job_1_get_attachments_response, job_2_get_attachments_response]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, attachments
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 new jobs created", output)
        self.assertIn("1 new documents imported", output)

        docs = CustomDocument.objects.filter(talentlink_attachment_id=111)
        self.assertEqual(
            docs.count(),
            1,
            msg="Documents with same talentlink_attachment_id should only be imported once.",
        )

    def test_job_with_no_attachment(self, mock_get_client):
        advertisements = [get_advertisement(talentlink_id=1, title="New title 1")]
        attachments = [{}]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, attachments
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("1 new jobs created", output)
        self.assertIn("0 new documents imported", output)

        job = TalentLinkJob.objects.get(talentlink_id=1)
        self.assertEqual(job.attachments.all().count(), 0)

    def test_multiple_attachments_are_imported(self, mock_get_client):
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]

        job_1_get_attachments_response = [
            get_attachment(id=111),
            get_attachment(id=112),
        ]

        attachments = [job_1_get_attachments_response]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, attachments
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 new documents imported", output)

        job = TalentLinkJob.objects.get(talentlink_id=1)
        self.assertEqual(job.attachments.all().count(), 2)

    def test_attachments_are_deleted_when_the_job_is(self, mock_get_client):
        job = TalentLinkJobFactory(talentlink_id=1, homepage=self.homepage)
        doc = DocumentFactory(talentlink_attachment_id=111)
        job.attachments.add(doc)
        job.save()

        job = TalentLinkJob.objects.filter(talentlink_id=1)
        doc = CustomDocument.objects.filter(talentlink_attachment_id=111)

        self.assertEqual(job.count(), 1)
        self.assertEqual(doc.count(), 1)

        job.delete()
        job = TalentLinkJob.objects.filter(talentlink_id=1)
        doc = CustomDocument.objects.filter(talentlink_attachment_id=111)

        self.assertEqual(job.count(), 0)
        self.assertEqual(
            doc.count(),
            0,
            msg="attached document should be deleted if its job is deleted",
        )

    def test_attachments_are_not_deleted_if_another_job_uses_them(
        self, mock_get_client
    ):

        job_1 = TalentLinkJobFactory(talentlink_id=1, homepage=self.homepage)
        doc_1 = DocumentFactory(talentlink_attachment_id=111)
        doc_2 = DocumentFactory(talentlink_attachment_id=222)
        job_1.attachments.add(doc_1)
        job_1.attachments.add(doc_2)
        job_1.save()

        job_2 = TalentLinkJobFactory(talentlink_id=2, homepage=self.homepage)
        job_2.attachments.add(doc_1)
        job_2.save()

        job = TalentLinkJob.objects.get(talentlink_id=1)
        doc = CustomDocument.objects.get(talentlink_attachment_id=111)

        self.assertEqual(doc.jobs.all().count(), 2)

        job.delete()
        job = TalentLinkJob.objects.filter(talentlink_id=1)
        doc = CustomDocument.objects.filter(talentlink_attachment_id=111)

        self.assertEqual(job.count(), 0)
        self.assertEqual(
            doc.count(),
            1,
            msg="attached document should be not deleted if it is being used elsewhere",
        )
        self.assertEqual(doc[0].jobs.all().count(), 1)

        job_2 = TalentLinkJob.objects.get(talentlink_id=2)
        self.assertEqual(job_2.attachments.first(), doc[0])


@mock.patch("bc.recruitment_api.management.commands.import_jobs.get_client")
@mock.patch(
    "bc.recruitment_api.management.commands.import_jobs.import_image_from_url",
    side_effect=mock_import_image_from_url,
)
class LogoTest(TestCase, ImportTestMixin):
    def setUp(self):
        ImportTestMixin.setUpRecruitmentHomePage(self)

    def test_logo_is_imported(self, mock_import_image_from_url, mock_get_client):
        original_image_count = CustomImage.objects.all().count()
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]

        job_1_get_logo_response = [get_logo(id="aaa")]
        job_2_get_logo_response = [get_logo(id="bbb")]
        logos = [job_1_get_logo_response, job_2_get_logo_response]

        mock_get_client.return_value = self.get_mocked_client(
            advertisements, logos=logos
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 new jobs created", output)
        self.assertIn("2 new images imported", output)
        self.assertEqual(CustomImage.objects.all().count(), original_image_count + 2)
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo,
            CustomImage.objects.get(talentlink_image_id="aaa"),
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo,
            CustomImage.objects.get(talentlink_image_id="bbb"),
        )

    def test_duplicate_logo_is_not_imported(
        self, mock_import_image_from_url, mock_get_client
    ):
        original_image_count = CustomImage.objects.all().count()
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]

        job_1_get_logo_response = [get_logo(id="aaa")]
        job_2_get_logo_response = [get_logo(id="aaa")]  # Duplicate
        logos = [job_1_get_logo_response, job_2_get_logo_response]

        mock_get_client.return_value = self.get_mocked_client(
            advertisements, logos=logos
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 new jobs created", output)
        self.assertIn("1 new images imported", output)
        self.assertEqual(CustomImage.objects.all().count(), original_image_count + 1)
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo,
            CustomImage.objects.get(talentlink_image_id="aaa"),
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo,
            CustomImage.objects.get(talentlink_image_id="aaa"),
        )

    def test_job_with_no_logo(self, mock_import_image_from_url, mock_get_client):
        original_image_count = CustomImage.objects.all().count()
        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
        ]

        logos = [
            {},  # No logo
        ]
        mock_get_client.return_value = self.get_mocked_client(
            advertisements, logos=logos
        )

        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("1 new jobs created", output)
        self.assertIn("0 new images imported", output)
        self.assertEqual(CustomImage.objects.all().count(), original_image_count)
        self.assertEqual(TalentLinkJob.objects.get(talentlink_id=1).logo, None)

    def test_job_logo_is_removed_if_removed_in_import(
        self, mock_import_image_from_url, mock_get_client
    ):
        job = TalentLinkJobFactory(talentlink_id=1)
        logo = ImageFactory(talentlink_image_id="aaa")
        job.logo = logo
        job.save()

        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
        ]
        logos = [
            {},
        ]

        mock_get_client.return_value = self.get_mocked_client(
            advertisements, logos=logos
        )
        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("1 existing jobs updated", output)
        self.assertIn("0 new images imported", output)
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo, None,
        )
        self.assertEqual(
            CustomImage.objects.filter(talentlink_image_id="aaa").count(), 0,
        )

    def test_used_job_logo_is_not_removed_if_removed_in_import(
        self, mock_import_image_from_url, mock_get_client
    ):
        job = TalentLinkJobFactory(talentlink_id=1)
        job_2 = TalentLinkJobFactory(talentlink_id=2)
        logo = ImageFactory(talentlink_image_id="aaa")
        job.logo = logo
        job.save()
        job_2.logo = logo
        job_2.save()

        advertisements = [
            get_advertisement(talentlink_id=1, title="New title 1"),
            get_advertisement(talentlink_id=2, title="New title 2"),
        ]
        job_1_get_logo_response = [get_logo(id="aaa")]
        job_2_get_logo_response = [{}]
        logos = [job_1_get_logo_response, job_2_get_logo_response]

        mock_get_client.return_value = self.get_mocked_client(
            advertisements, logos=logos
        )
        out = StringIO()
        call_command("import_jobs", stdout=out)
        out.seek(0)
        output = out.read()

        self.assertIn("2 existing jobs updated", output)
        self.assertIn("0 new images imported", output)
        self.assertEqual(
            CustomImage.objects.filter(talentlink_image_id="aaa").count(), 1,
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo, logo,
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo, None,
        )

    def test_logo_is_deleted_when_the_job_is(
        self, mock_import_image_from_url, mock_get_client
    ):
        job_1 = TalentLinkJobFactory(talentlink_id=1)
        job_2 = TalentLinkJobFactory(talentlink_id=2)
        logo_1 = ImageFactory()
        logo_2 = ImageFactory()
        job_1.logo = logo_1
        job_2.logo = logo_2
        job_1.save()
        job_2.save()

        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo,
            CustomImage.objects.get(id=logo_1.id),
        )

        job_1.delete()

        self.assertEqual(
            CustomImage.objects.filter(id=logo_1.id).count(),
            0,
            msg="Logo 1 should be deleted when Job 1 is.",
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo,
            CustomImage.objects.get(id=logo_2.id),
            msg="Job 2 and Logo 2 should be unaffected when Job 1 and Logo 1 is deleted.",
        )

    def test_logo_is_not_deleted_if_another_job_is_using_it(
        self, mock_import_image_from_url, mock_get_client
    ):
        job_1 = TalentLinkJobFactory(talentlink_id=1)
        job_2 = TalentLinkJobFactory(talentlink_id=2)
        logo = ImageFactory()
        job_1.logo = logo
        job_2.logo = logo
        job_1.save()
        job_2.save()

        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=1).logo,
            CustomImage.objects.get(id=logo.id),
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo,
            CustomImage.objects.get(id=logo.id),
        )

        job_1.delete()

        self.assertEqual(
            CustomImage.objects.filter(id=logo.id).count(),
            1,
            msg="Logo should not be deleted if it is still in use.",
        )
        self.assertEqual(
            TalentLinkJob.objects.get(talentlink_id=2).logo,
            CustomImage.objects.get(id=logo.id),
            msg="Job 2 and its logo should be unaffected when Job 1 is deleted.",
        )
