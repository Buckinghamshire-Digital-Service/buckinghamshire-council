from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtail.models import Page
from wagtail.test.utils import WagtailPageTests

from bc.standardpages.tests.fixtures import IndexPageFactory, InformationPageFactory

from ...standardpages.models import IndexPage, InformationPage
from ..models import HomePage
from .fixtures import HomePageFactory


class HomepageWagtailPageTests(WagtailPageTests):
    """
    Test page creation and infrastructure
    """

    def test_can_create_homepage(self):
        self.assertCanCreateAt(Page, HomePage)

    def test_can_only_create_homepage_under_root(self):
        self.assertAllowedParentPageTypes(
            HomePage,
            {Page},
            msg="HomePage should only be added as child of Page (root)",
        )


class HomePageModelTests(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=1)

        """
        Create a homepage which satisfies all required fields for positive test.
        """
        self.homepage = HomePageFactory.build_with_fk_objs_committed()
        self.root_page.add_child(instance=self.homepage)

        """
        Set up children pages for TOC
        5 IndexPage with 4 children InformationPage each
        """
        self.index_pages = []
        for i in range(5):
            index_page = IndexPageFactory.build()
            self.homepage.add_child(instance=index_page)
            self.index_pages.append(index_page)

            for j in range(4):
                information_page = InformationPageFactory.build()
                index_page.add_child(instance=information_page)

        """
        Set up information page as children of homepage
        """
        self.information_page = InformationPageFactory.build()
        self.homepage.add_child(instance=self.information_page)

    def test_hero_validation_when_no_image(self):
        with self.assertRaises(ValidationError):
            self.homepage.hero_image.delete()
            self.homepage.save()

    def test_hero_validation_when_no_strapline(self):
        with self.assertRaises(ValidationError):
            self.homepage.strapline = None
            self.homepage.save()

    def test_child_sections_types(self):
        # IndexPage can only be created as direct children of homepage, so we don't have to test for nested IndexPage
        self.assertEqual(
            len(self.homepage.child_sections),
            len(self.index_pages),
            msg="HomePage.child_sections should get IndexPage pages under the homepage, nothing more.",
        )
        self.assertTrue(
            len(self.homepage.child_sections) < len(self.homepage.get_children()),
            msg="Homepage.child_sections should not include pages that are not IndexPage.",
        )

    def test_child_sections_only_get_published_sections(self):
        self.index_pages[0].unpublish()
        self.assertEqual(
            len(self.homepage.child_sections),
            len(self.index_pages) - 1,
            msg="HomePage.child_sections should not include unpublished pages.",
        )

    def test_child_sections_only_get_public_sections(self):
        self.index_pages[0].view_restrictions.create(password="test")
        self.assertEqual(
            len(self.homepage.child_sections),
            len(self.index_pages) - 1,
            msg="HomePage.child_sections should not include private pages.",
        )

    def test_child_sections_sortorder(self):
        """
        Test that the queryset for IndexPage uses Wagtail explorer sort order
        """
        section_page = self.index_pages[0]
        original_order = list(
            self.homepage.child_sections.values_list("title", flat=True)
        )
        # Move self.index_pages[0]'s sortoder to last
        section_page.path = IndexPage._get_children_path_interval(self.homepage.path)[1]
        section_page.save()
        self.assertNotEqual(
            original_order,
            list(self.homepage.child_sections.values_list("title", flat=True)),
            msg="HomePage.child_sections should sort by page path (Wagtail explorer custom sort).",
        )

    """
    Testing IndexPage.featured_pages

    This is also covered in IndexPageModelTests(). However we are also testing here
    in case someone decides to change how it behaves on IndexPage and doesn't realise
    it also affects HomePage.
    """

    def test_child_sections_returns_max_3_grandchildren(self):
        # We have initially created 4 children under self.index_pages[0]
        self.assertNotEqual(
            len(self.index_pages[0].featured_pages),
            len(self.index_pages[0].get_children().live().public()),
            msg="IndexPage.featured_pages should be limited.",
        )
        self.assertLessEqual(
            len(self.index_pages[0].featured_pages),
            3,
            msg="IndexPage.featured_pages should be limited to max 3.",
        )

    def test_child_sections_returns_live_grandchildren(self):
        # Unpublish 2 of the 4 children
        children = self.index_pages[0].featured_pages
        children[0].unpublish()
        children[1].unpublish()
        self.assertNotEqual(
            len(self.index_pages[0].featured_pages),
            len(self.index_pages[0].get_children().public()[:3]),
            msg="IndexPage.featured_pages should not include unpublished pages.",
        )

    def test_child_sections_returns_public_grandchildren(self):
        section_page = self.index_pages[0]
        section_page.get_children().first().delete()  # delete 1 so we only have 3 to start with
        section_page.get_children().last().view_restrictions.create(password="test")
        self.assertEqual(
            len(section_page.featured_pages),
            len(section_page.get_children().live()) - 1,
            msg="IndexPage.featured_pages should not include private pages.",
        )

    def test_child_sections_grandchildren_sortorder(self):
        """
        Test that the queryset grandchildren uses Wagtail explorer sort order
        """
        section_page = self.index_pages[0]
        child_page = section_page.featured_pages.first()

        original_order = list(
            section_page.featured_pages.values_list("title", flat=True)
        )
        # Move childpage's sortoder to last
        child_page.path = InformationPage._get_children_path_interval(
            section_page.path
        )[1]
        child_page.save()

        self.assertNotEqual(
            original_order,
            list(section_page.featured_pages.values_list("title", flat=True)),
            msg="IndexPage.featured_pages should sort by page path (Wagtail explorer custom sort).",
        )
