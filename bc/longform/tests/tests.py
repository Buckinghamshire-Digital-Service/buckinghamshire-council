from http import HTTPStatus

from django.test import TestCase

import bs4

from bc.home.models import HomePage
from bc.longform.templatetags.longform_tags import generate_block_number
from bc.longform.tests.fixtures import LongformChapterPageFactory, LongformPageFactory


class BlockNumberTests(TestCase):
    def test_has_chapter_and_heading_numbers(self):
        result = generate_block_number(1, 2, 3, 4)
        self.assertEqual("1.3.4", result)

    def test_has_no_chapter_number(self):
        result = generate_block_number(None, 2, 3, 4)
        self.assertEqual("2.3.4", result)

    def test_has_no_chapter_or_heading_number(self):
        result = generate_block_number(None, None, 3, 4)
        self.assertEqual("3.4", result)

    def test_has_no_subheading_number(self):
        result = generate_block_number(1, 2, None, 4)
        self.assertEqual("1.4", result)

    def test_has_no_paragraph_number(self):
        result = generate_block_number(1, 2, 3, None)
        self.assertEqual("1.3", result)

    def test_has_only_paragraph_number(self):
        result = generate_block_number(None, None, None, 4)
        self.assertEqual("4", result)

    def test_has_no_numbers(self):
        result = generate_block_number(None, None, None, None)
        self.assertEqual("", result)


class TestLongformContentTitles(TestCase):
    """
    Test how chapter titles are displayed.

    The title of the parent Longform Content Page itself is the title to the whole
    section. If a chapter heading is set, it should not show up in the table of contents
    for the section. It should also not show up as the "previous" link that is displayed
    on the first chapter page. In either of those cases the chapter heading should be
    used if set.
    """

    @classmethod
    def setUpTestData(cls):
        cls.homepage = HomePage.objects.first()
        cls.longform_page = LongformPageFactory(
            parent=cls.homepage,
            title="The Longform Content page title",
            chapter_heading="The Longform Content page chapter heading",
        )
        cls.longform_chapter_page = LongformChapterPageFactory(
            parent=cls.longform_page, title="The Longform Chapter page title"
        )

    def test_longform_page_content_title(self):
        self.assertEqual(
            self.longform_page.content_title, self.longform_page.chapter_heading
        )

    def test_longform_page_content_title_default(self):
        longform_page = LongformPageFactory(
            parent=self.homepage,
            title="A longform content page with no chapter heading",
            chapter_heading="",
        )
        self.assertEqual(longform_page.content_title, longform_page.title)

    def test_longform_chapter_page_content_title(self):
        self.assertEqual(
            self.longform_chapter_page.content_title, self.longform_chapter_page.title
        )

    def test_longform_content_page_rendering(self):
        response = self.client.get(self.longform_page.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        # Page heading
        page_heading = soup.find("h1")
        self.assertEqual(page_heading.get_text(strip=True), self.longform_page.title)
        # Content heading
        content_heading = soup.find(class_="section").find("h2")
        self.assertEqual(
            content_heading.get_text(strip=True), self.longform_page.chapter_heading
        )
        # Table of contents
        table_of_contents = soup.find(class_="index-nav")
        self.assertIsNotNone(table_of_contents)
        first_toc_entry = table_of_contents.find(class_="index-nav__item")
        self.assertEqual(
            first_toc_entry.get_text(strip=True),
            "—" + self.longform_page.chapter_heading,
        )

    def test_longform_chapter_page_rendering(self):
        response = self.client.get(self.longform_chapter_page.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        # Page heading
        page_heading = soup.find("h1")
        self.assertEqual(page_heading.get_text(strip=True), self.longform_page.title)
        # Chapter heading
        content_heading = soup.find(class_="section").find("h2")
        self.assertEqual(
            content_heading.get_text(strip=True), self.longform_chapter_page.title
        )
        # Table of contents
        table_of_contents = soup.find(class_="index-nav")
        self.assertIsNotNone(table_of_contents)
        first_toc_entry = table_of_contents.find(class_="index-nav__item")
        self.assertEqual(
            first_toc_entry.get_text(strip=True),
            "—" + self.longform_page.chapter_heading,
        )
