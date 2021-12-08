import json

from django.test import SimpleTestCase, TestCase

from bc.home.models import HomePage
from bc.standardpages.tests.fixtures import InformationPageFactory
from bc.step_by_step.factories import StepByStepPageFactory
from bc.step_by_step.models import StepByStepReference
from bc.step_by_step.utils import FIND_INTERNAL_LINK, record_internal_links


def create_page_with_references(homepage):
    info_page_1 = InformationPageFactory.build()
    homepage.add_child(instance=info_page_1)
    info_page_2 = InformationPageFactory.build()
    homepage.add_child(instance=info_page_2)

    step_by_step_page = StepByStepPageFactory.build(
        steps=json.dumps(
            [
                {
                    "type": "step",
                    "value": {
                        "heading": "heading",
                        "information": f"""
                            <a id="{info_page_1.pk}" linktype="page">First page page</a>
                            <a id="{info_page_2.pk}" linktype="page">Another page</a>
                        """,
                    },
                }
            ]
        )
    )

    homepage.add_child(instance=step_by_step_page)

    return step_by_step_page, info_page_1, info_page_2


class InternalLinkRegexTests(SimpleTestCase):
    def get_matches(self, html):
        return FIND_INTERNAL_LINK.findall(html)

    def test_html_with_no_anchor_tags(self):
        html = """
        <div>
            This html doesn't have an anchor tag.
            <p>A small paragraph</p>
        </div>
        """
        self.assertCountEqual(self.get_matches(html), [])

    def test_html_with_no_Fage_anchor_tags(self):
        html = """
        <div>
            This html has only document anchor tags.
            <a id="1" linktype="document">Document link</a>
            <a href="www.example.com">External link</a>
        </div>
        """
        self.assertCountEqual(self.get_matches(html), [])

    def test_html_with_page_anchor_tags(self):
        html = """
        <div>
            This html has only document anchor tags.
            <a id="1" linktype="page">Page link</a>
            <a id="2" linktype="document">Document link</a>
            <a href="www.example.com">External link</a>
        </div>
        """
        self.assertCountEqual(self.get_matches(html), ["1"])


class RecordInternalLinkTests(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_add_references(self):
        step_by_step_page, info_page_1, info_page_2 = create_page_with_references(
            self.homepage
        )

        self.assertEqual(StepByStepReference.objects.count(), 0)

        record_internal_links(step_by_step_page)

        self.assertEqual(StepByStepReference.objects.count(), 2)
        self.assertCountEqual(
            StepByStepReference.objects.filter(
                step_by_step_page=step_by_step_page
            ).values_list("referenced_page_id", flat=True),
            [info_page_1.id, info_page_2.id],
        )

    def test_delete_references(self):
        step_by_step_page, _, info_page_2 = create_page_with_references(self.homepage)

        record_internal_links(step_by_step_page)

        self.assertEqual(StepByStepReference.objects.count(), 2)

        step_by_step_page.steps = json.dumps(
            [
                {
                    "type": "step",
                    "value": {
                        "heading": "heading",
                        "information": f"""
                    <a id="{info_page_2.pk}" linktype="page">Another page</a>
                    """,
                    },
                }
            ]
        )
        step_by_step_page.save()

        record_internal_links(step_by_step_page)

        self.assertEqual(StepByStepReference.objects.count(), 1)
        self.assertCountEqual(
            StepByStepReference.objects.filter(
                step_by_step_page=step_by_step_page
            ).values_list("referenced_page_id", flat=True),
            [info_page_2.id],
        )

    def test_update_references(self):
        step_by_step_page, _, info_page_2 = create_page_with_references(self.homepage)

        record_internal_links(step_by_step_page)

        self.assertEqual(StepByStepReference.objects.count(), 2)

        info_page_3 = InformationPageFactory.build()
        self.homepage.add_child(instance=info_page_3)

        step_by_step_page.steps = json.dumps(
            [
                {
                    "type": "step",
                    "value": {
                        "heading": "heading",
                        "information": f"""
                    <a id="{info_page_2.pk}" linktype="page">Another page</a>
                    <a id="{info_page_3.pk}" linktype="page">Third page</a>
                    """,
                    },
                }
            ]
        )
        step_by_step_page.save()

        record_internal_links(step_by_step_page)

        self.assertEqual(StepByStepReference.objects.count(), 2)
        self.assertCountEqual(
            StepByStepReference.objects.filter(
                step_by_step_page=step_by_step_page
            ).values_list("referenced_page_id", flat=True),
            [info_page_2.id, info_page_3.id],
        )


class LiveRelatedStepByStepPagesTest(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()

    def test_num_queries(self):
        step_by_step_page, info_page_1, info_page_2 = create_page_with_references(
            self.homepage
        )
        record_internal_links(step_by_step_page)

        step_by_step_page_2 = StepByStepPageFactory.build(
            steps=json.dumps(
                [
                    {
                        "type": "step",
                        "value": {
                            "heading": "heading",
                            "information": f"""
                                <a id="{info_page_1.pk}" linktype="page">First page page</a>
                                <a id="{info_page_2.pk}" linktype="page">Another page</a>
                            """,
                        },
                    }
                ]
            )
        )
        step_by_step_page_2.slug = "a" * 200

        self.homepage.add_child(instance=step_by_step_page_2)
        record_internal_links(step_by_step_page_2)

        with self.assertNumQueries(4):
            # 1 query for getting the referenced pages, 1 to get details of all referenced pages,
            # and 1 each to get the view_restricitions for each referenced page (2 referenced pages, hence 2)
            related_pages = info_page_1.live_related_stepbysteppages
            self.assertCountEqual(
                [related_page.step_by_step_page for related_page in related_pages],
                [step_by_step_page, step_by_step_page_2],
            )
