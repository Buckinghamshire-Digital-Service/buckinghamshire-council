import json

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from bc.recruitment.models import RecruitmentHomePage, TalentLinkJob


def is_recruitment_site(request):
    return request.site.root_page.specific.__class__ == RecruitmentHomePage


def get_search_filters(querystring):
    # Use this to add future filters
    # TODO: tie in with templatetags/jobs_search_filters.py
    filters = []
    category = {
        "name": "category",
        "filter_key": "subcategory__categories__slug",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
        "selected": None,
    }
    if querystring:
        category["selected"] = querystring.getlist(category["name"])
        category["selected"] = [x for x in category["selected"] if x.strip()]
        category["selected"].sort()
    filters.append(category)

    return filters


def get_current_search(querystring):
    """
    Returns search query and filters in request.GET as json string
    """
    search = {}

    if querystring.get("query", None):
        search["query"] = querystring.get("query", None)

    for filter in get_search_filters(querystring):
        if filter["selected"]:
            search[filter["name"]] = filter["selected"]

    return json.dumps(search)


def get_job_search_results(request):
    search_query = request.GET.get("query", None)

    if search_query:
        vector = (
            SearchVector("title", weight="A")
            # + SearchVector("short_description", weight="A")
            + SearchVector("searchable_location", weight="B")
            + SearchVector("description", weight="C")
        )
        query = SearchQuery(search_query, search_type="phrase")
        search_results = (
            TalentLinkJob.objects.annotate(rank=SearchRank(vector, query))
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

    else:
        # Order by newest job at top
        search_results = TalentLinkJob.objects.all().order_by("posting_start_date")

    # Process filters
    for filter in get_search_filters(request.GET):
        if filter["selected"]:
            search_results = search_results.filter(
                **{filter["filter_key"] + "__in": filter["selected"]}
            )

    return search_results
