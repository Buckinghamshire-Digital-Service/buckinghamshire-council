from django.test import TestCase
from django.urls import reverse
from wagtail.core.models import Site
from wagtail.tests.utils import WagtailTestUtils
from wagtail.tests.utils.form_data import streamfield, nested_form_data, rich_text

from bc.standardpages.models import InformationPage
from bc.standardpages.tests.fixtures import InformationPageFactory

from bc.navigation.models import NavigationSettings


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

    def setUp(self):
        self.login()

        self.default_site = Site.objects.get(is_default_site=True)
        self.root_page = self.default_site.root_page
        self.info_page = InformationPageFactory.build()
        self.root_page.add_child(instance=self.info_page)

        self.assertIsNotNone(self.info_page.id)

    def test_get_edit(self):
        response = self.get(site_pk=self.default_site.pk)
        self.assertEqual(response.status_code, 200)
        # there should be a menu item highlighted as active
        self.assertContains(response, "menu-active")

    def test_edit_columns_and_links(self):
        # Test create navigation with links and column
        form_data = nested_form_data(
            {
                "footer_columns": streamfield(
                    [
                        (
                            "column",
                            {
                                "heading": "Column Heading",
                                "content": rich_text("Column Content"),
                            },
                        )
                    ]
                ),
                "footer_links": streamfield(
                    [("link", {"page": self.info_page.id, "title": "Link Title"})]
                ),
            }
        )
        response = self.post(post_data=form_data, site_pk=self.default_site.pk,)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.status_code, 200)

        nav_setting = NavigationSettings.objects.get(site=self.default_site)
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


# Test create navigation with only columns
# Test create navigation with only links

# Test link title on page for navigation with only links
# Test column content on page for navigation with only column
# Test link title and column content on page for navigation with column and links
