from django.test import TestCase
from wagtail.core.models import Site
from wagtail.tests.utils.form_data import streamfield

from bc.standardpages.tests.fixtures import InformationPageFactory

from bc.navigation.models import NavigationSettings, LinkBlock


class NavigationSettingsTest(TestCase):
    def test_create_navigation_with_only_links(self):
        site = Site.objects.first()
        info_page = InformationPageFactory.build()
        link_block = ("link", {"page": info_page, "title": "Link Title"})
        nav_settings = NavigationSettings(footer_links=[link_block], site=site)

        nav_settings.full_clean()
        nav_settings.save()


# Test link title on page for navigation with only links
# Test create navigation with only columns
# Test column content on page for navigation with only column
# Test create navigation with links and column
# Test link title column content on page for navigation with only column
# Test create navigation without links or column fails
