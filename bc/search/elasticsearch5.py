import copy

from wagtail.search.backends.elasticsearch5 import Elasticsearch5SearchBackend

from bc.search.utils import get_synonyms


class SynonymSettingsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # print(get_synonyms())
        self.settings["settings"]["analysis"]["filter"]["synonym"] = {
            "type": "synonym",
            "synonyms": get_synonyms(),
        }


class SearchBackend(SynonymSettingsMixin, Elasticsearch5SearchBackend):
    settings = copy.deepcopy(Elasticsearch5SearchBackend.settings)
