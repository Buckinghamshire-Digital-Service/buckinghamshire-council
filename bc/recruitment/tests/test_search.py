from urllib.parse import unquote

from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Page, Site

import wagtail_factories

from bc.recruitment.constants import JOB_BOARD_CHOICES
from bc.recruitment.tests.fixtures import (
    RecruitmentHomePageFactory,
    TalentLinkJobFactory,
)
from bc.recruitment.utils import get_job_search_results


class SearchViewTest(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Job site (external)
        hero_image = wagtail_factories.ImageFactory()
        self.homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build(
                hero_image=hero_image, job_board=JOB_BOARD_CHOICES[0]
            )
        )
        self.site = Site.objects.create(
            hostname="jobs.example", port=80, root_page=self.homepage
        )

    def test_basic_search_behaviour(self):
        job = TalentLinkJobFactory.create(title="cycling", homepage=self.homepage)
        response = self.client.get(
            reverse("search") + "?query=cycling", SERVER_NAME=self.site.hostname
        )

        self.assertEqual(len(response.context["search_results"]), 1)
        self.assertIn(job, response.context["search_results"])

    def test_sql_injection(self):
        # This decodes to "schools\x00'||SLeeP(3)&&'1", where there's a NUL character
        # 0x00 between schools and the first inverted comma.
        query_string = unquote("category=schools%00%27||SLeeP(3)%26%26%271")
        querydict = QueryDict(query_string)
        results = get_job_search_results(querydict, self.homepage)
        try:
            results.first()  # Evaluate the search results
        except ValueError:
            self.fail(
                "SQL injection attempt caused an exception with job search results"
            )
