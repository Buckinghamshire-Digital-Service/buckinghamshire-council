from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.tests.utils import WagtailTestUtils

from bc.home.models import HomePage

from ..models import InformationPage
from .fixtures import IndexPageFactory, InformationPageFactory


class IndexPageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        """
        Create 1 IndexPage with 3 child_pages
        """
        homepage = HomePage.objects.first()
        self.index_page = IndexPageFactory.build()
        homepage.add_child(instance=self.index_page)

        self.index_page_children = []
        for i in range(3):
            subpage = InformationPageFactory.build()
            self.index_page.add_child(instance=subpage)
            self.index_page_children.append(subpage)

    def test_child_pages_only_returns_children_one_level_below(self):
        # Add a grandchild page
        grandchild = InformationPageFactory.build()
        self.index_page_children[0].add_child(instance=grandchild)

        self.assertEqual(
            len(self.index_page.child_pages),
            len(self.index_page_children),
            msg="IndexPage.child_pages should include child pages, but not all descendant pages.",
        )

    def test_child_pages_returns_live_children(self):
        self.index_page_children[0].unpublish()
        self.assertEqual(
            len(self.index_page.child_pages),
            len(self.index_page_children) - 1,
            msg="IndexPage.child_pages should only include live child pages, and not unpublished pages.",
        )

    def test_child_pages_returns_public_children(self):
        self.index_page_children[0].view_restrictions.create(password="test")
        self.assertEqual(
            len(self.index_page.child_pages),
            len(self.index_page_children) - 1,
            msg="IndexPage.child_pages should only include public child pages, and not private pages.",
        )

    def test_child_pages_sortorder(self):
        """
        Test that the queryset uses Wagtail explorer sort order
        """
        subpage = self.index_page_children[0]
        original_order = list(
            self.index_page.child_pages.values_list("title", flat=True)
        )
        # Move self.index_page_children[0]'s sortoder to last
        subpage.path = InformationPage._get_children_path_interval(
            self.index_page.path
        )[1]
        subpage.save()
        self.assertNotEqual(
            original_order,
            list(self.index_page.child_pages.values_list("title", flat=True)),
            msg="IndexPage.child_pages should sort by page path (Wagtail explorer custom sort).",
        )

    def test_featured_pages_returns_max_three_children(self):
        # Add additional child page to self.index_page
        new_page = InformationPageFactory.build()
        self.index_page.add_child(instance=new_page)

        self.assertEqual(
            len(self.index_page.get_children().live().public()),
            4,
            msg="Confirming we have 4 child pages in our test.",
        )
        self.assertEqual(
            len(self.index_page.featured_pages),
            3,
            msg="IndexPage.featured_pages should be limited to max 3.",
        )

    """
    Test featured_pages property

    Should pass if child_pages pass since featured_pages is based on child_pages.
    But we test this anyway in case the property no longer uses child_pages.
    """

    def test_featured_pages_only_returns_children_one_level_below(self):
        self.index_page.featured_pages[2].delete()  # Was 3
        old_length = len(self.index_page.featured_pages)  # Now 2
        grandchild = (
            InformationPageFactory.build()
        )  # Add 1 grandchild, we should still have 2 only
        self.index_page_children[0].add_child(instance=grandchild)
        self.assertEqual(
            len(self.index_page.featured_pages),
            old_length,
            msg="IndexPage.featured_pages should include child pages, but not other descendant pages.",
        )

    def test_featured_pages_returns_live_children(self):
        self.index_page_children[0].unpublish()
        self.assertEqual(
            len(self.index_page.featured_pages),
            len(self.index_page_children) - 1,  # Initially 3
            msg="IndexPage.featured_pages should only include live child pages, and not unpublished pages.",
        )

    def test_featured_pages_returns_public_children(self):
        self.index_page_children[0].view_restrictions.create(password="test")
        self.assertEqual(
            len(self.index_page.featured_pages),
            len(self.index_page_children) - 1,  # Initially 3
            msg="IndexPage.featured_pages should only include public child pages, and not private pages.",
        )

    def test_featured_pages_sortorder(self):
        """
        Test that the queryset uses Wagtail explorer sort order
        """
        subpage = self.index_page_children[0]
        original_order = list(
            self.index_page.featured_pages.values_list("title", flat=True)
        )
        # Move self.index_page_children[0]'s sortoder to last
        subpage.path = InformationPage._get_children_path_interval(
            self.index_page.path
        )[1]
        subpage.save()
        self.assertNotEqual(
            original_order,
            list(self.index_page.featured_pages.values_list("title", flat=True)),
            msg="IndexPage.featured_pages should sort by page path (Wagtail explorer custom sort).",
        )

    """
    Test ordinary_pages property

    Should pass if child_pages pass since ordinary_pages is based on child_pages.
    But we test this anyway in case the property no longer uses child_pages.
    """

    def test_ordinary_pages_does_not_return_featured_pages(self):
        # We only have 3 child pages, so shouldn't return any ordinary_pages
        self.assertEqual(
            len(self.index_page.ordinary_pages),
            0,
            msg="IndexPage.ordinary_pages should not return featured_pages.",
        )

    def test_ordinary_pages_only_returns_children_one_level_below(self):
        page_4 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_4)
        original_length = len(self.index_page.ordinary_pages)  # 1
        grandchild = InformationPageFactory.build()  # Add 1 grandchild
        self.index_page_children[0].add_child(instance=grandchild)
        self.assertEqual(
            len(self.index_page.ordinary_pages),
            original_length,
            msg="IndexPage.ordinary_pages should include child pages, but not other descendant pages.",
        )

    def test_ordinary_pages_returns_live_pages(self):
        page_4 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_4)
        page_5 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_5)

        self.assertEqual(
            len(self.index_page.ordinary_pages),
            2,
            msg="IndexPage.ordinary_pages should return live, public, child pages not returned by featured pages.",
        )

        page_4.unpublish()
        self.assertEqual(
            len(self.index_page.ordinary_pages),
            1,
            msg="IndexPage.ordinary_pages should not return unpublished pages.",
        )

    def test_ordinary_pages_returns_public_pages(self):
        page_4 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_4)
        page_5 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_5)

        page_4.view_restrictions.create(password="test")  # Set as private
        self.assertEqual(
            len(self.index_page.ordinary_pages),
            1,
            msg="IndexPage.ordinary_pages should not return private pages.",
        )

    def test_ordinary_pages_sortorder(self):
        """
        Test that the queryset uses Wagtail explorer sort order
        """
        page_4 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_4)
        page_5 = InformationPageFactory.build()
        self.index_page.add_child(instance=page_5)
        original_order = list(
            self.index_page.ordinary_pages.values_list("title", flat=True)
        )

        # Move page_4's sortoder to last
        page_4.path = InformationPage._get_children_path_interval(self.index_page.path)[
            1
        ]
        page_4.save()
        self.assertNotEqual(
            original_order,
            list(self.index_page.ordinary_pages.values_list("title", flat=True)),
            msg="IndexPage.ordinary_pages should sort by page path (Wagtail explorer custom sort).",
        )

    def test_redirect_field_sends_302_response(self):
        redirect_page = InformationPageFactory.build(
            redirect_to="https://www.example.com"
        )
        self.index_page.add_child(instance=redirect_page)

        response = self.client.get(redirect_page.url)
        self.assertEqual(response.status_code, 302)

    @override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
    def test_redirect_field_sends_normal_response_when_viewing_draft(self):
        redirect_page = InformationPageFactory.build(
            redirect_to="https://www.example.com"
        )
        self.index_page.add_child(instance=redirect_page)

        # Try getting page draft
        self.login()
        response = self.client.get(
            reverse("wagtailadmin_pages:view_draft", args=(redirect_page.id,))
        )
        self.assertEqual(response.status_code, 200)
