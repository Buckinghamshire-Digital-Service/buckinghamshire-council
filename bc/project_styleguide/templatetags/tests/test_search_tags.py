from django.test import TestCase

from bc.project_styleguide.templatetags.search_tags import is_news_page


class TestIsNewsPageTag(TestCase):
    def test_false_for_info_page(self):
        is_news_page(None)
