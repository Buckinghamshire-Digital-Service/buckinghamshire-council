import re
import uuid
from collections import namedtuple
from http import HTTPStatus

from django.test import TestCase

from wagtail.core.blocks import StreamValue

from bs4 import BeautifulSoup

from bc.home.models import HomePage

from ..blocks import (
    NumberedHeadingBlock,
    NumberedParagraphBlock,
    NumberedSubheadingBlock,
)
from ..templatetags.longform_tags import generate_block_number, process_block_numbers
from .fixtures import LongformChapterPageFactory, LongformPageFactory


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


SectionTestCase = namedtuple(
    "SectionTestCase", ["case", "id", "tagname", "css_class", "content", "number"],
)


class RenderedBlockNumberTests(TestCase):
    def get_rendered_sections(self, streamblock):
        rendered = process_block_numbers(streamblock)
        soup = BeautifulSoup(rendered, "html.parser")
        return soup.find_all(id=re.compile(r"^section-[\d,\.]*$"))

    def compare(self, rendered_sections, expected_sections):
        self.assertEqual(
            len(expected_sections),
            len(rendered_sections),
            "Unexpected number of rendered section blocks",
        )
        for section, test_case in zip(rendered_sections, expected_sections):
            with self.subTest(test_case.case):
                self.assertEqual(section["id"], test_case.id)
                self.assertEqual(section.name, test_case.tagname)
                self.assertIn(
                    test_case.css_class,
                    section["class"],
                    msg=f"{test_case.css_class} not found in classes",
                )
                self.assertIn(
                    test_case.content,
                    section.text,
                    msg=f"Expected content '{test_case.content}' not found",
                )
                # test that the number is present, respecting word boundaries
                number_regex = r"\b" + test_case.number.replace(r".", r"\.") + r"\s"
                self.assertRegex(section.text, number_regex)

    def test_expected_block_flow(self):
        streamblock = [
            # 1. My heading 1
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 1", id=str(uuid.uuid4),
            ),
            # 1.1. My subheading 1
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 1", id=str(uuid.uuid4),
            ),
            # 1.1.1. My paragraph 1
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 1", id=str(uuid.uuid4),
            ),
            # 1.1.2 My paragraph 2
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 2", id=str(uuid.uuid4),
            ),
            # 1.2. My subheading 2
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 2", id=str(uuid.uuid4),
            ),
            # 1.2.1. My paragraph 3
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 3", id=str(uuid.uuid4),
            ),
            # 2. My heading 2
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 2", id=str(uuid.uuid4),
            ),
            # 2.1. My subheading 3
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 3", id=str(uuid.uuid4),
            ),
            # 2.1.1. My paragraph 3
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 4", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial heading is numbered 1",
                id="section-1",
                tagname="h2",
                css_class="heading--l",
                content="My heading 1",
                number="1.",
            ),
            SectionTestCase(
                case="A subheading after a heading gets a second level number",
                id="section-1.1",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 1",
                number="1.1.",
            ),
            SectionTestCase(
                case="A paragraph after a nested subheading gets a third level number",
                id="section-1.1.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 1",
                number="1.1.1.",
            ),
            SectionTestCase(
                case="A second successive paragraph increments the previous paragraph's number",
                id="section-1.1.2",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 2",
                number="1.1.2.",
            ),
            SectionTestCase(
                case="A subheading following a more nested paragraph increments the second level number",
                id="section-1.2",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 2",
                number="1.2.",
            ),
            SectionTestCase(
                case="A subsequent nested paragraph resets the third level number",
                id="section-1.2.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 3",
                number="1.2.1.",
            ),
            SectionTestCase(
                case="A subsequent heading increments the top level number",
                id="section-2",
                tagname="h2",
                css_class="heading--l",
                content="My heading 2",
                number="2.",
            ),
            SectionTestCase(
                case="A subheading following a heading resets the second level number",
                id="section-2.1",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 3",
                number="2.1.",
            ),
            SectionTestCase(
                case="A subsequent nested paragraph resets only the third level number",
                id="section-2.1.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 4",
                number="2.1.1.",
            ),
        )

        self.compare(rendered_sections, expected_sections)

    def test_heading_with_preceding_paragraph(self):
        streamblock = [
            # 1. My paragraph 1
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 1", id=str(uuid.uuid4),
            ),
            # 2. My heading 1
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 1", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial paragraph gets a top level number",
                id="section-1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 1",
                number="1.",
            ),
            SectionTestCase(
                case="A heading following a paragraph will not start at 1",
                id="section-2",
                tagname="h2",
                css_class="heading--l",
                content="My heading 1",
                number="2.",
            ),
        )

        self.compare(rendered_sections, expected_sections)

    def test_heading_with_preceding_subheading(self):
        streamblock = [
            # 1. My subheading 1
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 1", id=str(uuid.uuid4),
            ),
            # 2. My heading 1
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 1", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial subheading gets a top level number",
                id="section-1",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 1",
                number="1.",
            ),
            SectionTestCase(
                case="A heading following a subheading will not start at 1",
                id="section-2",
                tagname="h2",
                css_class="heading--l",
                content="My heading 1",
                number="2.",
            ),
        )

        self.compare(rendered_sections, expected_sections)

    def test_subheading_with_preceding_paragraph(self):
        streamblock = [
            # 1. My paragraph 1
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 1", id=str(uuid.uuid4),
            ),
            # 2. My subheading 1
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 1", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial paragraph gets a top level number",
                id="section-1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 1",
                number="1.",
            ),
            SectionTestCase(
                case="A subheading following a paragraph will not start at 1",
                id="section-2",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 1",
                number="2.",
            ),
        )

        self.compare(rendered_sections, expected_sections)

    def test_badly_ordered_blocks(self):
        """
        Test that process_block_numbers does not repeat numbers and follows hierarchy.
        """
        streamblock = [
            # 1. My paragraph 1
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 1", id=str(uuid.uuid4),
            ),
            # 2. My subheading 1
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 1", id=str(uuid.uuid4),
            ),
            # 3. My heading 1
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 1", id=str(uuid.uuid4),
            ),
            # 3.1. My paragraph 2
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 2", id=str(uuid.uuid4),
            ),
            # 3.2. My subheading 2
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 2", id=str(uuid.uuid4),
            ),
            # 3.2.1. My paragraph 3
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 3", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial paragraph gets a top level number",
                id="section-1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 1",
                number="1.",
            ),
            SectionTestCase(
                case="A subheading following a paragraph gets a top level number >1",
                id="section-2",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 1",
                number="2.",
            ),
            SectionTestCase(
                case="A heading following lower level blocks gets a top level number >1",
                id="section-3",
                tagname="h2",
                css_class="heading--l",
                content="My heading 1",
                number="3.",
            ),
            SectionTestCase(
                case="A paragraph after a top level heading gets a second level number",
                id="section-3.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 2",
                number="3.1.",
            ),
            SectionTestCase(
                case="A nested subheading after a paragraph gets a second level number >x.1",
                id="section-3.2",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 2",
                number="3.2.",
            ),
            SectionTestCase(
                case="A nested paragraph in a nested subheading gets a third level number",
                id="section-3.2.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 3",
                number="3.2.1.",
            ),
        )

        self.compare(rendered_sections, expected_sections)

    def test_heading_with_preceding_subheading_containing_a_paragraph(self):
        streamblock = [
            # 1. My subheading 1
            StreamValue.StreamChild(
                NumberedSubheadingBlock(), "My subheading 1", id=str(uuid.uuid4),
            ),
            # 1.1 My paragraph 1
            StreamValue.StreamChild(
                NumberedParagraphBlock(), "My paragraph 1", id=str(uuid.uuid4),
            ),
            # 2. My heading 1
            StreamValue.StreamChild(
                NumberedHeadingBlock(), "My heading 1", id=str(uuid.uuid4),
            ),
        ]

        rendered_sections = self.get_rendered_sections(streamblock)

        expected_sections = (
            SectionTestCase(
                case="An initial subheading gets a top level number",
                id="section-1",
                tagname="h3",
                css_class="heading--m",
                content="My subheading 1",
                number="1.",
            ),
            SectionTestCase(
                case="A nested paragraph below a subheading gets a second level number",
                id="section-1.1",
                tagname="div",
                css_class="paragraph-block",
                content="My paragraph 1",
                number="1.1.",
            ),
            SectionTestCase(
                case="A subheading following a paragraph will not start at 1",
                id="section-2",
                tagname="h2",
                css_class="heading--l",
                content="My heading 1",
                number="2.",
            ),
        )

        self.compare(rendered_sections, expected_sections)


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
        soup = BeautifulSoup(response.content, "html.parser")
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
        soup = BeautifulSoup(response.content, "html.parser")
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
        # Previous page link
        prev_page_link = soup.find(class_="index-pagination__page-title")
        self.assertEqual(
            prev_page_link.get_text(strip=True), self.longform_page.chapter_heading
        )
