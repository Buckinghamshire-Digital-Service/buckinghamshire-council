from django.core.cache import caches

from bc.search.models import Term

cache = caches["default"]

SYNONYMS_CACHE_KEY = "searchbackend_synonyms"


def get_synonyms(force_update=False):
    if force_update:
        synonyms = None
    else:
        synonyms = cache.get(SYNONYMS_CACHE_KEY)

    if not synonyms:
        synonyms = [
            ", ".join(
                [term.canonical_term] + [synonym.lower() for synonym in term.synonyms]
            )
            for term in Term.objects.all()
        ]
        cache.set(SYNONYMS_CACHE_KEY, synonyms)

    if not synonyms:
        # Only necessary for Elasticsearch5 backend. The list can not be empty.
        # An empty list with the Elasticsearch5 backend will result in:
        # elasticsearch.exceptions.RequestError: RequestError(400, 'illegal_argument_exception', 'synonym requires either `synonyms` or `synonyms_path` to be configured')
        synonyms = [""]

    return synonyms
