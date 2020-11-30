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
    return synonyms
