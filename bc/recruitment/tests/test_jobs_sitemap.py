import datetime
import xml.etree.ElementTree as ET

from django.test import Client, TestCase, override_settings
from freezegun import freeze_time
from wagtail.models import Page, Site

from bc.recruitment.constants import JOB_BOARD_CHOICES

from .fixtures import RecruitmentHomePageFactory, TalentLinkJobFactory


def get_job_urls(site, job):
    urls = [
        site.root_page.full_url
        + site.root_page.reverse_subpage(
            "job_detail",
            args=(job.talentlink_id,),
        )
    ]
    if job.show_apply_button:
        urls.append(job.application_url)
    return urls


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

    @override_settings(
        ALLOWED_HOSTS=["jobs.example", "internal-jobs.example", "main.example"]
    )
    def test_fetch_particular_site_jobs(self):
        client = Client()

        instant = datetime.datetime(2020, 1, 29, 0, 0, tzinfo=datetime.timezone.utc)
        with freeze_time(instant):
            posting_start_date = instant - datetime.timedelta(days=1)
            posting_end_date = instant + datetime.timedelta(days=1)
            job_1 = TalentLinkJobFactory.create(
                title="cycling",
                homepage=self.homepage,
                posting_start_date=posting_start_date,
                posting_end_date=posting_end_date,
            )
            job_2 = TalentLinkJobFactory.create(
                title="cycling",
                homepage=self.homepage,
                posting_start_date=posting_start_date,
                posting_end_date=posting_end_date,
            )
            job_3 = TalentLinkJobFactory.create(
                title="cycling",
                homepage=self.homepage_internal,
                posting_start_date=posting_start_date,
                posting_end_date=posting_end_date,
            )

            # check that internal urls dont show up on external sitemap
            external_job_urls = [
                f"{self.site.root_url}/",
                *get_job_urls(self.site, job_1),
                *get_job_urls(self.site, job_2),
            ]
            recruitment_site_request = client.get(
                "/sitemap.xml", SERVER_NAME=self.site.hostname
            )
            response = ET.fromstring(recruitment_site_request.content)
            external_sitemap_urls = [child[0].text for child in response]
            self.assertCountEqual(external_sitemap_urls, external_job_urls)

            # check that external urls dont show up on internal sitemap
            internal_job_urls = [
                f"{self.site_internal.root_url}/",
                *get_job_urls(self.site_internal, job_3),
            ]
            recruitment_site_request = client.get(
                "/sitemap.xml", SERVER_NAME=self.site_internal.hostname
            )
            response = ET.fromstring(recruitment_site_request.content)
            internal_sitemap_urls = [child[0].text for child in response]
            self.assertCountEqual(internal_sitemap_urls, internal_job_urls)
