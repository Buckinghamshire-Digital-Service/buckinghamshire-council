import copy

from django.conf import settings

from wagtail.search.backends.elasticsearch7 import (
    Elasticsearch7SearchBackend,
    Elasticsearch7SearchQueryCompiler,
)

from bc.search.utils import get_synonyms


class ReduceBoostSearchQueryCompilerMixin:
    """
    Mixin for Elasticsearch query compilers that reduce the boost of a given
    content type.

    Currently the only content type that receives a negative boost is the
    NewsPage content type. The content type is hard coded. The boost reduction
    factor is pulled in from a setting. The setting allows to change the reduction
    factor without the need to change code.

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
                "negative_boost": settings.SEARCH_BOOST_FACTOR_NEWS_PAGE,
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
    ReduceBoostSearchQueryCompilerMixin, Elasticsearch7SearchQueryCompiler
):
    pass


class SearchBackend(SynonymSettingsMixin, Elasticsearch7SearchBackend):
    settings = copy.deepcopy(Elasticsearch7SearchBackend.settings)
    query_compiler_class = SearchQueryCompiler
