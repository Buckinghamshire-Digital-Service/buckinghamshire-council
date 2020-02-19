import json

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control
from django.views.generic.edit import FormView

from wagtail.core.models import Page
from wagtail.search.models import Query

from bc.recruitment.forms import SearchAlertSubscriptionForm
from bc.recruitment.models import (
    JobAlertSubscription,
    RecruitmentHomePage,
    TalentLinkJob,
)
from bc.utils.cache import get_default_cache_control_kwargs


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    template_path = "patterns/pages/search/search.html"

    # Recruitment site search
    if request.site.root_page.specific.__class__ == RecruitmentHomePage:
        template_path = "patterns/pages/search/search--jobs.html"
        search_results = get_jobs_search_results(request)

    # Main site search
    else:
        if search_query:
            search_results = Page.objects.live().search(search_query, operator="and")
            query = Query.get(search_query)
            # Record hit
            query.add_hit()

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


def get_jobs_search_results(request):
    search_query = request.GET.get("query", None)
    filter_job_category = request.GET.getlist("category")

    if search_query:
        vector = (
            SearchVector("title", weight="A")
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
        # Order by newest job at top
        search_results = TalentLinkJob.objects.all().order_by("posting_start_date")

    # Process filters
    if filter_job_category:
        search_results = search_results.filter(category__slug__in=filter_job_category)

    return search_results


class SearchAlertSubscriptionView(FormView):
    form_class = SearchAlertSubscriptionForm
    template_name = "patterns/pages/search/jobs_alert.html"
    # success_url = lazy_reverse('search:search')

    def get_serialized_search(self):
        #  eg. http://jobs.bc.local:8000/jobs_alert/?query=teacher&category=schools-early-years-support&category=it
        search = {}
        search["query"] = self.request.GET.get("query", None)
        search["category"] = self.request.GET.getlist("category")
        # If empty assumes subscribing to all new jobs?
        # TODO: display summary?
        return json.dumps(search)

    def form_valid(self, form):
        search = self.get_serialized_search()
        email = form.cleaned_data["email"]

        # Search if already exists and confirmed:
        try:
            subscription = JobAlertSubscription.objects.get(email=email, search=search)
            if subscription.confirmed:
                # Tell user they're already subscribed
                # TODO
                # import pdb; pdb.set_trace()
                pass

        except JobAlertSubscription.DoesNotExist:
            subscription = JobAlertSubscription(email=email, search=search)
            subscription.full_clean()
            subscription.save()

        self.send_mail(subscription)
        return super(SearchAlertSubscriptionView, self).form_valid(form)

    def send_mail(self, subscription):
        # TODO: email token to user
        import pdb

        pdb.set_trace()
        pass
