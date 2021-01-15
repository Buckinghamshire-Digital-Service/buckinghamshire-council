from django.conf import settings
from django.core.management import call_command

from wagtail.search.backends import get_search_backend

ORIGINAL_INDEX_NAME = settings.WAGTAILSEARCH_BACKENDS["default"].get("INDEX")


def is_elasticsearch_backend(backend):
    return hasattr(backend, "es")


def update_search_index():
    call_command("update_index")


def delete_test_indices_from_elasticsearch():
    backend = get_search_backend()
    if is_elasticsearch_backend(backend):
        test_indices = backend.es.indices.get(get_index_name_for_test() + "*")
        for test_index in test_indices.keys():
            backend.es.indices.delete(test_index)


def get_search_settings_for_test():
    search_backend_settings = settings.WAGTAILSEARCH_BACKENDS
    backend = get_search_backend()
    if is_elasticsearch_backend(backend):
        search_backend_settings["default"]["INDEX"] = get_index_name_for_test()
    return search_backend_settings


def get_index_name_for_test():
    if ORIGINAL_INDEX_NAME:
        return "test_" + ORIGINAL_INDEX_NAME
