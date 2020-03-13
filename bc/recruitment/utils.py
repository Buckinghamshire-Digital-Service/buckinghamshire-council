import json

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from bc.recruitment.constants import JOB_FILTERS
from bc.recruitment.models import JobCategory, RecruitmentHomePage, TalentLinkJob


def is_recruitment_site(request):
    return isinstance(request.site.root_page.specific, RecruitmentHomePage)


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

    # Process 'hide schools and early years job'
    search_results_with_schools = search_results
    if querydict.get("hide_schools_and_early_years", False):
        schools_and_early_years_categories = (
            JobCategory.get_school_and_early_years_slugs()
        )
        search_results = search_results.exclude(
            subcategory__categories__slug__in=schools_and_early_years_categories
        )

    # Process filters
    for filter in JOB_FILTERS:
        # QueryDict.update() used in send_job_alerts.py adds the values as list instead of multivalue dict.
        if isinstance(querydict.get(filter["name"]), list):
            selected = querydict.get(filter["name"])
        else:
            selected = querydict.getlist(
                filter["name"]
            )  # will return empty list if not found

        if selected:
            search_results = search_results.filter(
                **{
                    filter["filter_key"] + "__in": selected
                }  # TODO: make case insensitive
            )

    return search_results, search_results_with_schools
