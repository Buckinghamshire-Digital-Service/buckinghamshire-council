from django.conf import settings
from django.test import TestCase, override_settings

from wagtail.models import Page, Site

from bc.recruitment.constants import JOB_BOARD_CHOICES

from .fixtures import RecruitmentHomePageFactory, TalentLinkJobFactory

INTERNAL_HOSTNAME = "example-internal.com"
EXTERNAL_HOSTNAME = "example.com"


class TestApplyConfigKey(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        # Job site (external)
        self.homepage = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                job_board=JOB_BOARD_CHOICES[0]
            )
        )
        self.site = Site.objects.create(
            hostname="example.com", port=80, root_page=self.homepage
        )

        # Internal job site
        self.homepage_internal = self.root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                job_board=JOB_BOARD_CHOICES[1]
            )
        )
        self.site_internal = Site.objects.create(
            hostname="example-internal.com",
            port=80,
            root_page=self.homepage_internal,
        )

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        WAGTAILADMIN_BASE_URL="http://localhost/",
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
        WAGTAILADMIN_BASE_URL="http://localhost/",
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
        WAGTAILADMIN_BASE_URL="http://localhost/",
    )
    def test_404_when_job_id_is_badly_formatted(self):
        """This is mainly to ensure that IDs which previously raised a 500 don't."""
        for job_id in [
            None,
            "abc",
            1,
            "QQPFK026203F3VBQBV7V779XA-175679'A=0",  # a seen SQL injection attack
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

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        WAGTAILADMIN_BASE_URL="http://localhost/",
    )
    def test_view_when_job_id_does_not_exist(self):
        for job_id in [
            "abc-123",
            "LONGSTRING-123456",
        ]:
            with self.subTest(job_id=job_id):
                resp = self.client.get(
                    self.homepage.full_url
                    + self.homepage.reverse_subpage("apply")
                    + "?jobId="
                    + str(job_id),
                    HTTP_HOST=self.site.hostname + ":80",
                )
                self.assertEqual(resp.status_code, 200)

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        WAGTAILADMIN_BASE_URL="http://localhost/",
    )
    def test_sidebar_normally_shown(self):
        job = TalentLinkJobFactory.create(
            title="puncture patcher", homepage=self.homepage
        )
        resp = self.client.get(
            job.application_url, HTTP_HOST=self.site.hostname + ":80"
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["show_sidebar"], True)

    @override_settings(
        ALLOWED_HOSTS=[
            "localhost",
            "testserver",
            INTERNAL_HOSTNAME,
            EXTERNAL_HOSTNAME,
        ],
        WAGTAILADMIN_BASE_URL="http://localhost/",
    )
    def test_sidebar_not_shown_when_job_id_does_not_exist(self):
        resp = self.client.get(
            self.homepage.full_url
            + self.homepage.reverse_subpage("apply")
            + "?jobId=abc-123",
            HTTP_HOST=self.site.hostname + ":80",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["show_sidebar"], False)
