import json

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from bc.recruitment.constants import JOB_FILTERS
from bc.recruitment.models import RecruitmentHomePage, TalentLinkJob


def is_recruitment_site(request):
    return request.site.root_page.specific.__class__ == RecruitmentHomePage


def get_current_search(querydict):
    """
    Returns search query and filters in request.GET as json string
    """
    search = {}

    if querydict.get("query", None):
        search["query"] = querydict.get("query", None)

    # Loop through our filters so we don't just store any query params
    for filter in JOB_FILTERS:
        selected = querydict.getlist(filter["name"])
        if selected:
            selected = list(dict.fromkeys(selected))  # Remove duplicate options
            search[filter["name"]] = sorted(selected)  # Sort options alphabetically

    return json.dumps(search)


def get_job_search_results(querydict, queryset=None):
    if queryset is None:
        queryset = TalentLinkJob.objects.all()
    search_query = querydict.get("query", None)

    if search_query:
        vector = (
            SearchVector("title", weight="A")
            # + SearchVector("short_description", weight="A")
            + SearchVector("searchable_location", weight="B")
            + SearchVector("description", weight="C")
        )
        query = SearchQuery(search_query, search_type="phrase")
        search_results = (
            queryset.annotate(rank=SearchRank(vector, query))
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

    else:
        # Order by newest job at top
        search_results = queryset.order_by("posting_start_date")

    # Process filters
    for filter in JOB_FILTERS:
        selected = querydict.getlist(filter["name"])
        if selected:
            search_results = search_results.filter(
                **{filter["filter_key"] + "__in": selected}
            )

    return search_results
