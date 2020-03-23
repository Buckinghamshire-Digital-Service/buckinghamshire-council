from django.test import TestCase, override_settings

from ..client import get_client


# @override_settings(
#     CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
# )
class TestCleanedData(TestCase):
    def test_connection(self):

        client = get_client()
