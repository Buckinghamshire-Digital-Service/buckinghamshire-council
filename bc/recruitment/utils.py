from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from bc.recruitment.models import RecruitmentHomePage, TalentLinkJob


def is_recruitment_site(request):
    return request.site.root_page.specific.__class__ == RecruitmentHomePage


def get_jobs_search_results(request):
    search_query = request.GET.get("query", None)
    filter_job_category = request.GET.getlist("category")

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
    # TODO: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
    if filter_job_category:
        search_results = search_results.filter(
            subcategory__categories__slug__in=filter_job_category
        )

    return search_results
