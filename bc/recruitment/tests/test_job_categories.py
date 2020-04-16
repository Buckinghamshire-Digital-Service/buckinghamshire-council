from django.test import TestCase
from django.utils.text import slugify

from wagtail.core.models import Page

from bc.recruitment.constants import JOB_BOARD_CHOICES
from bc.recruitment.models import JobCategory
from bc.recruitment.tests.fixtures import (
    JobCategoryFactory,
    JobSubcategoryFactory,
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)

# Job category title to match dummy Job Group in get_advertisement() fixture
FIXTURE_JOB_SUBCATEGORY_TITLE = "Schools & Early Years - Support"


class JobCategorySlugTest(TestCase):
    def test_job_category_autogenerates_slug(self):
        JobCategoryFactory(title="My title")
        self.assertEqual(
            JobCategory.objects.filter(slug=slugify("My title")).count(), 1
        )

    def test_job_category_unique_slug(self):
        job_categories = [
            JobCategoryFactory(title="My title"),
            JobCategoryFactory(title="My title"),
            JobCategoryFactory(title="My title"),
        ]
        self.assertEqual(len(set([jc.slug for jc in job_categories])), 3)

    def test_job_category_retains_slug(self):
        job_category = JobCategoryFactory(title="My title")
        job_category.slug = "custom-slug"
        job_category.save()
        self.assertEqual(job_category.slug, "custom-slug")
        job_category.title = "New title"
        job_category.save()
        self.assertEqual(job_category.slug, "custom-slug")


class JobCategoryAndJobSubcategoryGroupingTest(TestCase):
    def setUp(self):
        """
        Set up 5 subcategories and 2 categories
        """
        self.talentlinkjobs = []
        self.subcategories = []
        self.categories = []

        self.root_page = Page.objects.get(id=1)
        self.homepage = RecruitmentHomePageFactory.build_with_fk_objs_committed(
            job_board=JOB_BOARD_CHOICES[0]
        )
        self.root_page.add_child(instance=self.homepage)
        self.homepage_internal = RecruitmentHomePageFactory.build_with_fk_objs_committed(
            job_board=JOB_BOARD_CHOICES[1]
        )
        self.root_page.add_child(instance=self.homepage_internal)

        for i in range(4):
            subcat = JobSubcategoryFactory.build()
            subcat.save()
            # Add jobs for each subcategory according to its index (eg. self.subcategories[2] gets 2 jobs)
            for j in range(i):
                job = TalentLinkJobFactory.build(homepage=self.homepage)
                job.subcategory = subcat
                job.save()
                self.talentlinkjobs.append(job)

            self.subcategories.append(subcat)
        for i in range(2):
            cat = JobCategoryFactory.build()
            cat.save()
            self.categories.append(cat)

    def test_can_assign_multiple_subcategories_to_category(self):
        cat = self.categories[0]

        # Confirm cat has no subcategory to start with
        self.assertEqual(cat.subcategories.all().count(), 0)

        # Add 2 subcategories to cat
        cat.subcategories.add(self.subcategories[0], self.subcategories[1])
        self.assertEqual(cat.subcategories.all().count(), 2)

    def test_can_assign_subcategory_to_multiple_categories(self):
        subcat = self.subcategories[0]

        # Confirm subcat has no category to start with
        self.assertEqual(subcat.categories.all().count(), 0)

        # Add to 2 categories
        self.categories[0].subcategories.add(subcat)
        self.categories[1].subcategories.add(subcat)
        self.assertEqual(subcat.categories.all().count(), 2)

    def test_subcategory_get_categories_list(self):
        subcat = self.subcategories[0]

        # Test when empty categories
        self.assertEqual(subcat.get_categories_list(), [])

        # Add to 2 categories
        self.categories[0].subcategories.add(subcat)
        self.categories[1].subcategories.add(subcat)
        self.assertEqual(
            subcat.get_categories_list(),
            [self.categories[0].title, self.categories[1].title],
        )

    def test_category_get_subcategories_list(self):
        cat = self.categories[0]

        # Test when empty subcategories
        self.assertEqual(cat.get_subcategories_list(), [])

        # Add to 2 subcategories
        cat.subcategories.add(self.subcategories[0], self.subcategories[1])
        self.assertEqual(
            cat.get_subcategories_list(),
            [self.subcategories[0].title, self.subcategories[1].title],
        )

    def test_get_categories_summary_when_no_category_exists(self):
        self.categories[0].delete()
        self.categories[1].delete()
        self.assertEqual(JobCategory.get_categories_summary().count(), 0)

    def test_get_categories_summary_when_empty_subcategory(self):
        # We haven't assigned any subcategory to the categories yet, so should return empty
        self.assertEqual(JobCategory.get_categories_summary().count(), 0)

    def test_get_categories_summary_when_subcategory_has_no_job(self):
        self.categories[0].subcategories.add(
            self.subcategories[0]
        )  # this subcategory has 0 jobs
        self.assertEqual(JobCategory.get_categories_summary().count(), 0)

    def test_get_categories_summary(self):
        # Assign categories
        self.categories[0].subcategories.add(
            self.subcategories[0]
        )  # this subcategory has 0 jobs
        self.categories[1].subcategories.add(
            self.subcategories[1]
        )  # this subcategory has 1 job

        # Should return just self.categories[1] since self.categories[0] has 0 jobs.
        summary = JobCategory.get_categories_summary()
        self.assertEqual(summary.count(), 1)
        self.assertEqual(summary[0]["category"], self.categories[1].id)
        self.assertEqual(summary[0]["count"], 1)

    def test_get_categories_summary_respects_job_board(self):
        self.categories[1].subcategories.add(
            self.subcategories[1]
        )  # this subcategory has 1 job

        summary = JobCategory.get_categories_summary(homepage=self.homepage)
        self.assertEqual(summary.count(), 1)

        # Should return nothing since the jobs in setup are all external jobs (JOB_BOARD_CHOICES[0])
        summary = JobCategory.get_categories_summary(homepage=self.homepage_internal)
        self.assertEqual(summary.count(), 0)

        # Create internal job
        job = TalentLinkJobFactory(homepage=self.homepage_internal)
        job.subcategory = self.subcategories[1]
        job.save()

        summary = JobCategory.get_categories_summary(homepage=self.homepage_internal)
        self.assertEqual(summary.count(), 1)

    def test_get_categories_summary_ranking(self):
        # Assign categories
        self.categories[0].subcategories.add(
            self.subcategories[2]
        )  # this subcategory has 2 jobs
        self.categories[1].subcategories.add(
            self.subcategories[3]
        )  # this subcategory has 3 jobs

        summary = JobCategory.get_categories_summary()
        self.assertEqual(summary.count(), 2)
        self.assertEqual(summary[0]["category"], self.categories[1].id)
        self.assertEqual(summary[0]["count"], 3)
        self.assertEqual(summary[1]["category"], self.categories[0].id)
        self.assertEqual(summary[1]["count"], 2)

    def test_get_categories_with_overlap_subcategories(self):
        # Assign categories
        self.categories[0].subcategories.add(
            self.subcategories[2]
        )  # this subcategory has 2 jobs
        self.categories[0].subcategories.add(
            self.subcategories[3]
        )  # this subcategory has 3 jobs
        self.categories[1].subcategories.add(
            self.subcategories[3]
        )  # this subcategory has 3 jobs

        summary = JobCategory.get_categories_summary()
        self.assertEqual(summary.count(), 2)
        self.assertEqual(summary[0]["category"], self.categories[0].id)
        self.assertEqual(summary[0]["count"], 3 + 2)
        self.assertEqual(summary[1]["category"], self.categories[1].id)
        self.assertEqual(summary[1]["count"], 3)
