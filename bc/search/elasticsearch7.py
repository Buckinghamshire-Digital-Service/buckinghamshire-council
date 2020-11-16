import copy

from wagtail.search.backends.elasticsearch7 import Elasticsearch7SearchBackend

from bc.search.elasticsearch5 import SynonymSettingsMixin
from bc.search.utils import get_synonyms


class SearchBackend(SynonymSettingsMixin, Elasticsearch7SearchBackend):
    settings = copy.deepcopy(Elasticsearch7SearchBackend.settings)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings["settings"]["analysis"]["filter"]["synonym"] = {
            "type": "synonym",
            "synonyms": get_synonyms(),
        }
