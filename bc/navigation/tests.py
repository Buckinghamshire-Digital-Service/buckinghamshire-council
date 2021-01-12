from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Site
from wagtail.tests.utils import WagtailTestUtils
from wagtail.tests.utils.form_data import nested_form_data, rich_text, streamfield

from bc.navigation.models import NavigationSettings
from bc.standardpages.models import InformationPage
from bc.standardpages.tests.fixtures import InformationPageFactory


class NavigationSettingsModelTest(TestCase):
    def test_create_navigation_with_only_links(self):
        site = Site.objects.first()
        root_page = site.root_page
        info_page = InformationPageFactory.build()
        root_page.add_child(instance=info_page)
        link_block = ("link", {"page": info_page, "title": "Link Title"})

        nav_settings = NavigationSettings.objects.create(
            footer_links=[link_block], site=site
        )


class NavigationSettingViewTest(TestCase, WagtailTestUtils):

    # From: https://github.com/wagtail/wagtail/blob/a726c93df489fc14a393047e8eb8f6b864fde089/wagtail/contrib/settings/tests/test_admin.py#L47
    def get(self, site_pk=1, params={}, setting=NavigationSettings):
        url = self.edit_url(setting=setting, site_pk=site_pk)
        return self.client.get(url, params)

    # From: https://github.com/wagtail/wagtail/blob/a726c93df489fc14a393047e8eb8f6b864fde089/wagtail/contrib/settings/tests/test_admin.py#L47
    def post(self, site_pk=1, post_data={}, setting=NavigationSettings):
        url = self.edit_url(setting=setting, site_pk=site_pk)
        return self.client.post(url, post_data)

    # From: https://github.com/wagtail/wagtail/blob/a726c93df489fc14a393047e8eb8f6b864fde089/wagtail/contrib/settings/tests/test_admin.py#L47
    def edit_url(self, setting, site_pk=1):
        args = [setting._meta.app_label, setting._meta.model_name, site_pk]
        return reverse("wagtailsettings:edit", args=args)

    def get_form_data(self, include_cloumns, include_links):
        column_data = (
            "column",
            {"heading": "Column Heading", "content": rich_text("Column Content")},
        )
        link_data = ("link", {"page": self.info_page.id, "title": "Link Title"})

        included_column_data = []
        if include_cloumns:
            included_column_data.append(column_data)
        included_link_data = []
        if include_links:
            included_link_data.append(link_data)

        combined_data = {
            "footer_columns": streamfield(included_column_data),
            "footer_links": streamfield(included_link_data),
        }
        return nested_form_data(combined_data)

    def get_site_navigation_settings(self):
        return NavigationSettings.objects.get(site=self.default_site)

    def setUp(self):
        self.login()

        self.default_site = Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)

        self.assertIsNotNone(self.info_page.id)

    def test_initial_site_navigation_settings(self):
        with self.assertRaises(NavigationSettings.DoesNotExist):
            self.get_site_navigation_settings()

    def test_get_edit(self):
        response = self.get(site_pk=self.default_site.pk)
        self.assertEqual(response.status_code, 200)
        # there should be a menu item highlighted as active
        self.assertContains(response, "menu-active")

    def test_create_navigation_settings_with_columns_and_links(self):
        # Test create navigation with links and column
        form_data = self.get_form_data(include_cloumns=True, include_links=True)

        response = self.post(post_data=form_data, site_pk=self.default_site.pk,)

        self.assertEqual(
            response.status_code, 302
        )  # Reload the page with GET after receiving POST. Therefore its a redirect.
        nav_setting = self.get_site_navigation_settings()
        self.assertNotEqual(nav_setting.footer_links.stream_data, [])
        self.assertNotEqual(nav_setting.footer_columns.stream_data, [])
        linked_info_page = InformationPage.objects.get(
            pk=nav_setting.footer_links[0].value["page"].id
        )
        self.assertEqual(linked_info_page, self.info_page)
        self.assertEqual(nav_setting.footer_links[0].value["title"], "Link Title")
        self.assertEqual(linked_info_page, self.info_page)
        self.assertEqual(
            nav_setting.footer_columns[0].value["heading"], "Column Heading"
        )
        self.assertIn(
            "Column Content", nav_setting.footer_columns[0].value["content"].source
        )

    def test_create_navigation_settings_with_columns_wo_links(self):
        # Test create navigation with only columns
        form_data = self.get_form_data(include_cloumns=True, include_links=False)

        response = self.post(post_data=form_data, site_pk=self.default_site.pk,)

        self.assertEqual(
            response.status_code, 302
        )  # Reload the page with GET after receiving POST. Therefore its a redirect.
        nav_setting = self.get_site_navigation_settings()
        self.assertEqual(nav_setting.footer_links.stream_data, [])
        self.assertNotEqual(nav_setting.footer_columns.stream_data, [])
        self.assertEqual(
            nav_setting.footer_columns[0].value["heading"], "Column Heading"
        )
        self.assertIn(
            "Column Content", nav_setting.footer_columns[0].value["content"].source
        )

    def test_create_navigation_settings_wo_columns_with_links(self):
        # Test create navigation with only links
        form_data = self.get_form_data(include_cloumns=False, include_links=True)

        response = self.post(post_data=form_data, site_pk=self.default_site.pk,)

        self.assertEqual(
            response.status_code, 302
        )  # Reload the page with GET after receiving POST. Therefore its a redirect.
        nav_setting = self.get_site_navigation_settings()
        self.assertNotEqual(nav_setting.footer_links.stream_data, [])
        self.assertEqual(nav_setting.footer_columns.stream_data, [])
        linked_info_page = InformationPage.objects.get(
            pk=nav_setting.footer_links[0].value["page"].id
        )
        self.assertEqual(linked_info_page, self.info_page)
        self.assertEqual(nav_setting.footer_links[0].value["title"], "Link Title")

    def test_created_columns_and_links_displayed(self):
        form_data = self.get_form_data(include_cloumns=True, include_links=True)
        self.post(
            post_data=form_data, site_pk=self.default_site.pk,
        )

        response = self.client.get(self.root_page.url)

        self.assertContains(response, "Link Title")
        self.assertContains(response, self.info_page.url)
        self.assertContains(response, "Column Heading")
        self.assertContains(response, "Column Content")

    def test_created_columns_displayed(self):
        form_data = self.get_form_data(include_cloumns=True, include_links=False)
        self.post(
            post_data=form_data, site_pk=self.default_site.pk,
        )

        response = self.client.get(self.root_page.url)

        self.assertNotContains(response, "Link Title")
        self.assertNotContains(response, self.info_page.url)
        self.assertContains(response, "Column Heading")
        self.assertContains(response, "Column Content")

    def test_created_links_displayed(self):
        form_data = self.get_form_data(include_cloumns=False, include_links=True)
        self.post(
            post_data=form_data, site_pk=self.default_site.pk,
        )

        response = self.client.get(self.root_page.url)

        self.assertContains(response, "Link Title")
        self.assertContains(response, self.info_page.url)
        self.assertNotContains(response, "Column Heading")
        self.assertNotContains(response, "Column Content")
