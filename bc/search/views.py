from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control

from wagtail.core.models import Page
from wagtail.search.models import Query

from bc.recruitment.models import RecruitmentHomePage, TalentLinkJob
from bc.utils.cache import get_default_cache_control_kwargs


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    template_path = "patterns/pages/search/search.html"
    is_jobs_search = False

    # Check if this is the recruitment site
    if request.site.root_page.specific.__class__ == RecruitmentHomePage:
        template_path = "patterns/pages/search/search--jobs.html"
        is_jobs_search = True

    # Search
    if search_query:
        if is_jobs_search:
            vector = (
                SearchVector("title", weight="A")
                + SearchVector("category", weight="B")
                + SearchVector("searchable_location", weight="B")
                + SearchVector("description", weight="C")
            )
            query = SearchQuery(search_query, search_type="phrase")
            search_results = (
                TalentLinkJob.objects.annotate(rank=SearchRank(vector, query))
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )

        else:
            search_results = Page.objects.live().search(search_query, operator="and")
            query = Query.get(search_query)
            # Record hit
            query.add_hit()

    else:
        if is_jobs_search:
            # Order by newest job at top
            search_results = TalentLinkJob.objects.all().order_by("posting_start_date")
        else:
            search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, settings.DEFAULT_PER_PAGE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    response = TemplateResponse(
        request,
        template_path,
        {"search_query": search_query, "search_results": search_results},
    )
    # Instruct FE cache to not cache when the search query is present.
    # It's so hits get added to the database and results include newly
    # added pages.
    if search_query:
        add_never_cache_headers(response)
    else:
        patch_cache_control(response, **get_default_cache_control_kwargs())
    return response
