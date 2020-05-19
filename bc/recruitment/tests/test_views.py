from django.conf import settings
from django.test import TestCase, override_settings

from wagtail.core.models import Page, Site

import wagtail_factories

from bc.recruitment.constants import JOB_BOARD_CHOICES

from .fixtures import RecruitmentHomePageFactory, TalentLinkJobFactory

INTERNAL_HOSTNAME = "example-internal.com"
EXTERNAL_HOSTNAME = "example.com"


class TestApplyConfigKey(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)
        hero_image = wagtail_factories.ImageFactory()

        # Job site (external)
        self.homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build(
                hero_image=hero_image, job_board=JOB_BOARD_CHOICES[0]
            )
        )
        self.site = Site.objects.create(
            hostname="example.com", port=80, root_page=self.homepage
        )

        # Internal job site
        self.homepage_internal = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build(
                hero_image=hero_image, job_board=JOB_BOARD_CHOICES[1]
            )
        )
        self.site_internal = Site.objects.create(
            hostname="example-internal.com", port=80, root_page=self.homepage_internal,
        )

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        TALENTLINK_APPLY_CONFIG_KEY_EXTERNAL="the-external-one",
        TALENTLINK_APPLY_CONFIG_KEY_INTERNAL="the-internal-one",
    )
    def test_internal_key_var(self):
        job = TalentLinkJobFactory.create(
            title="lock picker", homepage=self.homepage_internal
        )
        resp = self.client.get(
            job.application_url, HTTP_HOST=self.site_internal.hostname + ":80"
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            settings.TALENTLINK_APPLY_CONFIG_KEY_INTERNAL, resp.content.decode()
        )

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        TALENTLINK_APPLY_CONFIG_KEY_EXTERNAL="the-external-one",
        TALENTLINK_APPLY_CONFIG_KEY_INTERNAL="the-internal-one",
    )
    def test_external_key_var(self):
        job = TalentLinkJobFactory.create(
            title="sausage stuffer", homepage=self.homepage
        )
        resp = self.client.get(
            job.application_url, HTTP_HOST=self.site.hostname + ":80"
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            settings.TALENTLINK_APPLY_CONFIG_KEY_EXTERNAL, resp.content.decode()
        )

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
    )
    def test_404_when_job_id_is_badly_formatted(self):
        """This is mainly to ensure that IDs which previously raised a 500 don't."""
        for job_id in [
            None,
            "abc",
            1,
            "abc-123",
        ]:
            with self.subTest(job_id=job_id):
                resp = self.client.get(
                    self.homepage.full_url
                    + self.homepage.reverse_subpage("apply")
                    + "?jobId="
                    + str(job_id),
                    HTTP_HOST=self.site.hostname + ":80",
                )
                self.assertEqual(resp.status_code, 404)
