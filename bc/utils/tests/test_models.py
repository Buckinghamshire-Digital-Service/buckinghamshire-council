from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.core.models import Page, Site

import wagtail_factories

from bc.home.tests.fixtures import HomePageFactory
from bc.recruitment.tests.fixtures import RecruitmentHomePageFactory
from bc.standardpages.tests.fixtures import IndexPageFactory, InformationPageFactory
from bc.utils.constants import BASE_PAGE_TEMPLATE, BASE_PAGE_TEMPLATE_RECRUITMENT

MAIN_HOSTNAME = "foo.example.com"
RECRUITMENT_HOSTNAME = "bar.example.com"


@override_settings(ALLOWED_HOSTS=[MAIN_HOSTNAME, RECRUITMENT_HOSTNAME])
class BasePageTemplateTest(TestCase):
    def setUp(self):
        root_page = Page.objects.get(id=1)

        self.homepage = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=self.homepage)
        self.main_site = Site.objects.create(
            hostname=MAIN_HOSTNAME, port=80, root_page=self.homepage
        )

        hero_image = wagtail_factories.ImageFactory()
        self.recruitment_homepage = root_page.add_child(
            instance=RecruitmentHomePageFactory.build(
                title="Jobs", hero_image=hero_image
            )
        )
        self.recruitment_site = Site.objects.create(
            hostname=RECRUITMENT_HOSTNAME, port=80, root_page=self.recruitment_homepage
        )
        self.page_factories = [InformationPageFactory, IndexPageFactory]

    def test_main_homepage_uses_main_site(self):
        """This is mainly a test that this test case is viable."""
        response = self.client.get("/", SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.context["request"].site, self.main_site)

    def test_recruitment_homepage_uses_recruitment_site(self):
        """This is mainly a test that this test case is viable."""
        response = self.client.get("/", SERVER_NAME=RECRUITMENT_HOSTNAME)
        self.assertEqual(response.context["request"].site, self.recruitment_site)

    def test_main_homepage_uses_main_base(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE):
            response = self.client.get("/", SERVER_NAME=MAIN_HOSTNAME)
            self.assertEqual(response.status_code, 200)

    def test_recruitment_homepage_uses_recruitment_base(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE_RECRUITMENT):
            response = self.client.get("/", SERVER_NAME=RECRUITMENT_HOSTNAME)
            self.assertEqual(response.status_code, 200)

    def test_child_of_main_site_uses_main_base(self):
        for Factory in self.page_factories:
            with self.subTest(page_type=Factory._meta.model):
                page = Factory.build()
                self.homepage.add_child(instance=page)
                with self.assertTemplateUsed(BASE_PAGE_TEMPLATE):
                    response = self.client.get(page.url, SERVER_NAME=MAIN_HOSTNAME)
                    self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.context["base_page_template"], BASE_PAGE_TEMPLATE
                )

    def test_child_of_recruitment_site_uses_recruitment_base(self):
        for Factory in self.page_factories:
            with self.subTest(page_type=Factory._meta.model):
                page = Factory.build()
                self.recruitment_homepage.add_child(instance=page)
                with self.assertTemplateUsed(BASE_PAGE_TEMPLATE_RECRUITMENT):
                    response = self.client.get(
                        page.url, SERVER_NAME=RECRUITMENT_HOSTNAME
                    )
                    self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.context["base_page_template"],
                    BASE_PAGE_TEMPLATE_RECRUITMENT,
                )

    def test_main_404_uses_main_site(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE):
            response = self.client.get("/this_should_404/", SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context["base_page_template"], BASE_PAGE_TEMPLATE)

    def test_recruitment_404_uses_recruitment_site(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE_RECRUITMENT):
            response = self.client.get(
                "/this_should_404/", SERVER_NAME=RECRUITMENT_HOSTNAME
            )
            self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.context["base_page_template"], BASE_PAGE_TEMPLATE_RECRUITMENT
        )

    def test_main_search_uses_main_site(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE):
            response = self.client.get(reverse("search"), SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["base_page_template"], BASE_PAGE_TEMPLATE)

    def test_recruitment_search_uses_recruitment_site(self):
        with self.assertTemplateUsed(BASE_PAGE_TEMPLATE_RECRUITMENT):
            response = self.client.get(
                reverse("search"), SERVER_NAME=RECRUITMENT_HOSTNAME
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["base_page_template"], BASE_PAGE_TEMPLATE_RECRUITMENT
        )
