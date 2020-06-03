from django.test import RequestFactory, TestCase

from wagtail.core.models import Page, Site

from bc.recruitment.constants import JOB_BOARD_CHOICES
from bc.recruitment.templatetags.jobs_search_filters import jobs_search_filters
from bc.recruitment.tests.fixtures import (
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)

# Job category title to match dummy Job Group in get_advertisement() fixture
FIXTURE_JOB_SUBCATEGORY_TITLE = "Schools & Early Years - Support"


class SalaryFiltersTest(TestCase):
    salary_filter_index = 4  # just to DRY the changes if the filters ever change

    def setUp(self):
        """
        Set up 5 subcategories and 2 categories
        """
        self.root_page = Page.objects.get(id=1)
        self.homepage = RecruitmentHomePageFactory.build_with_fk_objs_committed(
            job_board=JOB_BOARD_CHOICES[0]
        )
        self.root_page.add_child(instance=self.homepage)
        self.site = Site.objects.create(root_page=self.homepage)

    def test_fifth_filter_is_salary(self):
        request = RequestFactory().get(self.homepage.url)
        request.site = self.site
        context = jobs_search_filters(request)

        self.assertEqual(
            context["filters"][self.salary_filter_index]["key"], "searchable_salary",
        )

    def test_pound_sign_values_ordered_first(self):
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="£1")
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Everything")
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Anything")
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="£2")
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Zero")

        request = RequestFactory().get(self.homepage.url)
        request.site = self.site
        context = jobs_search_filters(request)

        self.assertEqual(
            [
                foo["label"]
                for foo in context["filters"][self.salary_filter_index]["options"]
            ],
            ["£1", "£2", "Anything", "Everything", "Zero"],
        )

    def test_pound_signs_later_in_the_string_ordered_first(self):
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="£1")
        TalentLinkJobFactory(
            homepage=self.homepage, searchable_salary="£30,001 - £40,000"
        )
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Everything")
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Up to £4")
        TalentLinkJobFactory(
            homepage=self.homepage, searchable_salary="£20,001 - £30,000"
        )
        TalentLinkJobFactory(homepage=self.homepage, searchable_salary="Zero")

        request = RequestFactory().get(self.homepage.url)
        request.site = self.site
        context = jobs_search_filters(request)

        self.assertEqual(
            [
                foo["label"]
                for foo in context["filters"][self.salary_filter_index]["options"]
            ],
            [
                "Up to £4",
                "£1",
                "£20,001 - £30,000",
                "£30,001 - £40,000",
                "Everything",
                "Zero",
            ],
        )
