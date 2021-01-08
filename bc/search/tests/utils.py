from django.conf import settings
from django.core.management import call_command

from wagtail.search.backends import get_search_backend

TESTSEARCH_INDEX_NAME = "bc_test"


def is_elasticsearch_backend(backend=None):
    if backend is None:
        backend = get_search_backend()
    return hasattr(backend, "es")


def update_search_index():
    call_command("update_index")


def delete_test_indices_from_elasticsearch():
    backend = get_search_backend()
    if is_elasticsearch_backend(backend):
        test_indices = backend.es.indices.get(TESTSEARCH_INDEX_NAME + "*")
        for test_index in test_indices.keys():
            backend.es.indices.delete(test_index)


search_backend_settings = settings.WAGTAILSEARCH_BACKENDS
if is_elasticsearch_backend():
    search_backend_settings["default"]["INDEX"] = TESTSEARCH_INDEX_NAME
