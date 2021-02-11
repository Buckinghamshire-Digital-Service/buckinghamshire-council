import copy

from wagtail.search.backends.elasticsearch7 import (
    Elasticsearch7SearchBackend,
    Elasticsearch7SearchQueryCompiler,
)

from bc.search.elasticsearch5 import (
    SynonymSettingsMixin,
    ReduceBoostSearchQueryCompilerMixin,
)


class SearchQueryCompiler(
    ReduceBoostSearchQueryCompilerMixin, Elasticsearch7SearchQueryCompiler
):
    pass


class SearchBackend(SynonymSettingsMixin, Elasticsearch7SearchBackend):
    settings = copy.deepcopy(Elasticsearch7SearchBackend.settings)
    query_compiler_class = SearchQueryCompiler
