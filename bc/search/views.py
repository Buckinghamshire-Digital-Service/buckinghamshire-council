import json

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control
from django.utils.timezone import now
from django.views.generic.base import View
from django.views.generic.edit import FormView

from wagtail.core.models import Page
from wagtail.search.models import Query

from bc.recruitment.forms import SearchAlertSubscriptionForm
from bc.recruitment.models import JobAlertSubscription
from bc.recruitment.utils import get_jobs_search_results, is_recruitment_site
from bc.utils.cache import get_default_cache_control_kwargs


class SearchView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("query", None)
        page = request.GET.get("page", 1)
        template_path = "patterns/pages/search/search.html"
        context = {}

        # Recruitment site search
        if is_recruitment_site(request):
            template_path = "patterns/pages/search/search--jobs.html"
            search_results = get_jobs_search_results(request)
            context["job_alert_form"] = SearchAlertSubscriptionForm

        # Main site search
        else:
            if search_query:
                search_results = Page.objects.live().search(
                    search_query, operator="and"
                )
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

        context.update({"search_query": search_query, "search_results": search_results})

        response = TemplateResponse(request, template_path, context,)

        # Instruct FE cache to not cache when the search query is present.
        # It's so hits get added to the database and results include newly
        # added pages.
        if search_query:
            add_never_cache_headers(response)
        else:
            patch_cache_control(response, **get_default_cache_control_kwargs())
        return response

    def post(self, request, *args, **kwargs):
        if not is_recruitment_site(request):
            return

        form = SearchAlertSubscriptionForm(data=request.POST)
        if form.is_valid():
            import pdb

            pdb.set_trace()
            pass
            # TODO: process
        else:
            # TODO: return to search page with warning
            pass


class SearchAlertSubscriptionView(FormView):
    form_class = SearchAlertSubscriptionForm
    template_name = "patterns/pages/search/job_alert.html"
    # success_url = lazy_reverse('search:search')

    def get_serialized_search(self):
        # TODO: refactor to centralise the logic for this so
        # can be used together with search view, and only one place to update when adding new filters
        # http://jobs.bc.local:8000/job_alert/?query=school&category=work-experiencetraineeshipinternship&category=transport-economy-environment
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
            else:
                # Treat this as a new subscription request and
                # refresh created date to give this more time to be confirmed.
                subscription.created = now()

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
