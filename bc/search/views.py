from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control
from django.utils.timezone import now
from django.views.generic.base import View

from wagtail.core.models import Page
from wagtail.search.models import Query

from bc.recruitment.forms import SearchAlertSubscriptionForm
from bc.recruitment.models import JobAlertSubscription
from bc.recruitment.utils import (
    get_current_search,
    get_job_search_results,
    is_recruitment_site,
)
from bc.utils.cache import get_default_cache_control_kwargs

JOB_ALERT_STATUSES = {
    "STATUS_ALREADY_SUBSCRIBED": "already_subscribed",
    "STATUS_EMAIL_SENT": "email_sent",
    "STATUS_CONFIRMED": "confirmed",
    "STATUS_LINK_EXPIRED": "link_expired",
    "STATUS_UNSUBSCRIBED": "unsubscribed",
}


class SearchView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("query", None)
        page = request.GET.get("page", 1)
        template_path = "patterns/pages/search/search.html"
        context = {}

        # Recruitment site search
        if is_recruitment_site(request):
            template_path = "patterns/pages/search/search--jobs.html"
            search_results = get_job_search_results(querydict=request.GET)
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
        """
        Job alert subscription
        """
        if not is_recruitment_site(request):
            return

        form = SearchAlertSubscriptionForm(data=request.POST)

        if form.is_valid():
            # e.g. query=school&category=work-experiencetraineeshipinternship&category=transport-economy-environment
            search = get_current_search(request.GET)
            email = form.cleaned_data["email"]
            context = {"STATUSES": JOB_ALERT_STATUSES}

            # Search if already exists and confirmed:
            try:
                subscription = JobAlertSubscription.objects.get(
                    email=email, search=search
                )
                if subscription.confirmed:
                    # Tell user they're already subscribed
                    context.update(
                        {
                            "title": "You are already subscribed",
                            "status": context["STATUSES"]["STATUS_ALREADY_SUBSCRIBED"],
                        }
                    )
                    response = TemplateResponse(
                        request,
                        "patterns/pages/jobs_alert/subscription_processed.html",
                        context,
                    )
                    return response
                else:
                    # Treat this as a new subscription request and
                    # refresh created date to give this more time to be confirmed.
                    subscription.created = now()

            except JobAlertSubscription.DoesNotExist:
                subscription = JobAlertSubscription(email=email, search=search)
                subscription.full_clean()
                subscription.save()

            subscription.send_confirmation_email(request)
            context.update(
                {
                    "title": "Thank you",
                    "status": context["STATUSES"]["STATUS_EMAIL_SENT"],
                }
            )
            response = TemplateResponse(
                request,
                "patterns/pages/jobs_alert/subscription_processed.html",
                context,
            )
            return response


class JobAlertConfirmView(View):
    def get(self, request, *args, **kwargs):
        token = self.kwargs["token"]
        context = {"STATUSES": JOB_ALERT_STATUSES}

        try:
            subscription = JobAlertSubscription.objects.get(token=token)
        except JobAlertSubscription.DoesNotExist:
            context.update(
                {
                    "title": "Subscription not found",
                    "status": context["STATUSES"]["STATUS_LINK_EXPIRED"],
                }
            )
        else:
            subscription.confirmed = True
            subscription.save()
            context.update(
                {
                    "title": "Job alert subscription confirmed",
                    "status": context["STATUSES"]["STATUS_CONFIRMED"],
                }
            )

        response = TemplateResponse(
            request, "patterns/pages/jobs_alert/subscription_processed.html", context,
        )
        return response


class JobAlertUnsubscribeView(View):
    # TODO:  Future feature: display all subscriptions for this email address and
    # allow user to unsubscribe from all or selected.
    def get(self, request, *args, **kwargs):
        token = self.kwargs["token"]
        context = {"STATUSES": JOB_ALERT_STATUSES}

        try:
            subscription = JobAlertSubscription.objects.get(token=token)
        except JobAlertSubscription.DoesNotExist:
            context.update(
                {
                    "title": "Subscription not found",
                    "status": context["STATUSES"]["STATUS_LINK_EXPIRED"],
                }
            )
        else:
            subscription.delete()
            context.update(
                {
                    "title": "Job alert unsubscribed",
                    "status": context["STATUSES"]["STATUS_UNSUBSCRIBED"],
                }
            )

        response = TemplateResponse(
            request, "patterns/pages/jobs_alert/unsubscribe.html", context,
        )
        return response
