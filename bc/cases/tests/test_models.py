from unittest import skip

from django.test import TestCase


# FIXME this needs to work
@skip
class CaseFormPageTest(TestCase):
    def test_page_loads_when_client_not_configured(self):
        pass
