from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from bc.home.tests.fixtures import HomePageFactory
from bc.recruitment.tests.fixtures import RecruitmentHomePageFactory
from bc.standardpages.tests.fixtures import IndexPageFactory, InformationPageFactory
from bc.utils.constants import BASE_PAGE_TEMPLATE, BASE_PAGE_TEMPLATE_RECRUITMENT

from .factories import SystemMessageFactory

MAIN_HOSTNAME = "foo.example.com"
RECRUITMENT_HOSTNAME = "bar.example.com"


@override_settings(ALLOWED_HOSTS=[MAIN_HOSTNAME, RECRUITMENT_HOSTNAME])
class BasePageTemplateTest(WagtailTestUtils, TestCase):
    def setUp(self):
        root_page = Page.objects.get(id=1)

        self.homepage = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=self.homepage)
        self.main_site = Site.objects.create(
            hostname=MAIN_HOSTNAME, port=80, root_page=self.homepage
        )

        self.recruitment_homepage = root_page.add_child(
            instance=RecruitmentHomePageFactory.build_with_fk_objs_committed(
                title="Jobs"
            )
        )
        self.recruitment_site = Site.objects.create(
            hostname=RECRUITMENT_HOSTNAME, port=80, root_page=self.recruitment_homepage
        )
        self.page_factories = [InformationPageFactory, IndexPageFactory]

    def test_main_homepage_uses_main_site(self):
        """This is mainly a test that this test case is viable."""
        request = RequestFactory().get("/", SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(Site.find_for_request(request), self.main_site)

    @override_settings(WAGTAILADMIN_BASE_URL="http://localhost/")
    def test_recruitment_homepage_uses_recruitment_site(self):
        """This is mainly a test that this test case is viable."""
        request = RequestFactory().get("/", SERVER_NAME=RECRUITMENT_HOSTNAME)
        self.assertEqual(Site.find_for_request(request), self.recruitment_site)

    def test_main_homepage_uses_main_base(self):
        response = self.client.get("/", SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)

    @override_settings(WAGTAILADMIN_BASE_URL="http://localhost/")
    def test_recruitment_homepage_uses_recruitment_base(self):
        response = self.client.get("/", SERVER_NAME=RECRUITMENT_HOSTNAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE)

    def test_child_of_main_site_uses_main_base(self):
        for Factory in self.page_factories:
            with self.subTest(page_type=Factory._meta.model):
                page = Factory.build()
                self.homepage.add_child(instance=page)
                response = self.client.get(page.url, SERVER_NAME=MAIN_HOSTNAME)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE)
                self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
                self.assertEqual(
                    response.context["base_page_template"], BASE_PAGE_TEMPLATE
                )

    @override_settings(WAGTAILADMIN_BASE_URL="http://localhost/")
    def test_child_of_recruitment_site_uses_recruitment_base(self):
        for Factory in self.page_factories:
            with self.subTest(page_type=Factory._meta.model):
                page = Factory.build()
                self.recruitment_homepage.add_child(instance=page)
                response = self.client.get(page.url, SERVER_NAME=RECRUITMENT_HOSTNAME)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
                self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE)
                self.assertEqual(
                    response.context["base_page_template"],
                    BASE_PAGE_TEMPLATE_RECRUITMENT,
                )

    def test_main_404_uses_main_site(self):
        response = self.client.get("/this_should_404/", SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
        self.assertEqual(response.context["base_page_template"], BASE_PAGE_TEMPLATE)

    @override_settings(WAGTAILADMIN_BASE_URL="http://localhost/")
    def test_recruitment_404_uses_recruitment_site(self):
        response = self.client.get(
            "/this_should_404/", SERVER_NAME=RECRUITMENT_HOSTNAME
        )
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE)
        self.assertEqual(
            response.context["base_page_template"], BASE_PAGE_TEMPLATE_RECRUITMENT
        )

    def test_main_search_uses_main_site(self):
        response = self.client.get(reverse("search"), SERVER_NAME=MAIN_HOSTNAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
        self.assertEqual(response.context["base_page_template"], BASE_PAGE_TEMPLATE)

    @override_settings(WAGTAILADMIN_BASE_URL="http://localhost/")
    def test_recruitment_search_uses_recruitment_site(self):
        response = self.client.get(reverse("search"), SERVER_NAME=RECRUITMENT_HOSTNAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_PAGE_TEMPLATE_RECRUITMENT)
        self.assertTemplateNotUsed(response, BASE_PAGE_TEMPLATE)
        self.assertEqual(
            response.context["base_page_template"], BASE_PAGE_TEMPLATE_RECRUITMENT
        )

    @override_settings(
        ALLOWED_HOSTS=[MAIN_HOSTNAME, RECRUITMENT_HOSTNAME, "oof.example.com"]
    )
    def test_default_site_handling(self):
        """
        Checks that the global_vars context processor handles requests without breaking,
        regardless of whether a default site is set
        """
        # We're testing the /admin/ page, so we need to log in first
        self.user = self.login()

        # Test that no site is returned for requests with unknown server names,
        # when no default site is set
        default_site = Site.objects.get(is_default_site=True)
        default_site.is_default_site = False
        default_site.save()
        request = RequestFactory().get("/admin/", SERVER_NAME="oof.example.com")
        self.assertIsNone(Site.find_for_request(request))

        # Test that fallback values are added by the context processor
        # for requests with unknown server names, when no default site is set
        response = self.client.get("/admin/", SERVER_NAME="oof.example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_pensions_site"], False)
        self.assertEqual(response.context["base_page_template"], BASE_PAGE_TEMPLATE)

        # Test that the default site is returned for requests with unknown server names,
        # when one is set
        self.recruitment_site.is_default_site = True
        self.recruitment_site.save()
        request = RequestFactory().get("/admin/", SERVER_NAME="oof.example.com")
        self.assertEqual(Site.find_for_request(request), self.recruitment_site)

        # Test that site-specific values are added by the context processor
        # for requests with unknown server names, when a default site is set
        response = self.client.get("/admin/", SERVER_NAME="oof.example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_pensions_site"], False)
        self.assertEqual(
            response.context["base_page_template"], BASE_PAGE_TEMPLATE_RECRUITMENT
        )


class NoSearchResultsTemplateTest(TestCase):
    def setUp(self):
        root_page = Page.objects.get(id=1)

        homepage = HomePageFactory.build_with_fk_objs_committed()
        root_page.add_child(instance=homepage)
        self.main_site = Site.objects.create(
            hostname=MAIN_HOSTNAME, port=80, root_page=homepage
        )

    def test_valid_message_wildcard(self):
        message_model = SystemMessageFactory(
            site=self.main_site,
            body_no_search_results="This includes {searchterms}, which is valid.",
        )
        try:
            message_model.clean_fields()
        except ValidationError:
            self.fail("Including {searchterms} in the message failed validation")

    def test_invalid_message_wildcard(self):
        message_model = SystemMessageFactory(
            site=self.main_site,
            body_no_search_results="This includes an invalid {wildcard}.",
        )
        with self.assertRaises(ValidationError):
            message_model.clean_fields()
