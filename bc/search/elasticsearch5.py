import copy

from wagtail.search.backends.elasticsearch5 import (
    Elasticsearch5SearchQueryCompiler,
    Elasticsearch5SearchBackend,
)

from bc.search.utils import get_synonyms


class ReduceBoostSearchQueryCompilerMixin:
    """
    Mixin for Elasticsearch query compilers that reduce the boost of a given
    content type.

    All credit for this goes to @karl.
    See also:
    https://torchbox.slack.com/archives/C0251P48T/p1613040022098500?thread_ts=1613039057.098200&cid=C0251P48T

    Currently the only content type that receives a negative boost is the
    NewsPage content type. The type and the negative boost factor are hardcoded.

    If necessary, this could potentially be opened for extension or made more
    flexible.
    See also:
    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html

    """

    def get_inner_query(self):
        return {
            "boosting": {
                "positive": super().get_inner_query(),
                "negative": {"term": {"content_type": "news.NewsPage"}},
                "negative_boost": 0.5,
            }
        }


class SynonymSettingsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings["settings"]["analysis"]["filter"]["synonym"] = {
            "type": "synonym",
            "synonyms": get_synonyms(),
        }


class SearchQueryCompiler(
    ReduceBoostSearchQueryCompilerMixin, Elasticsearch5SearchQueryCompiler
):
    pass


class SearchBackend(SynonymSettingsMixin, Elasticsearch5SearchBackend):
    settings = copy.deepcopy(Elasticsearch5SearchBackend.settings)
    query_compiler_class = SearchQueryCompiler
