from unittest import skip

from django.test import TestCase, override_settings

# from ..client import get_client


@skip
@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)
class TestCleanedData(TestCase):
    def test_connection(self):
        # get_client()
        pass
