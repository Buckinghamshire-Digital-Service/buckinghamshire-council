import copy

from wagtail.search.backends.elasticsearch7 import Elasticsearch7SearchBackend

from bc.search.elasticsearch5 import SynonymSettingsMixin


class SearchBackend(SynonymSettingsMixin, Elasticsearch7SearchBackend):
    settings = copy.deepcopy(Elasticsearch7SearchBackend.settings)
