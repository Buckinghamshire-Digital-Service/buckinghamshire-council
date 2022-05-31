from itertools import chain

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, CharField, OuterRef, Subquery, When
from django.http import QueryDict
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from wagtail.core.models import Page, Site
from wagtail.search.models import Query

from bc.blogs.models import BlogHomePage
from bc.blogs.utils import get_blogs_search_results, is_blogs_search
from bc.campaigns.models import CampaignIndexPage, CampaignPage
from bc.recruitment.forms import SearchAlertSubscriptionForm
from bc.recruitment.models import JobAlertSubscription
from bc.recruitment.utils import (
    get_current_search,
    get_job_search_results,
    is_recruitment_site,
)
from bc.utils.cache import get_default_cache_control_kwargs
from bc.utils.models import SystemMessagesSettings

JOB_ALERT_STATUSES = {
    "STATUS_ALREADY_SUBSCRIBED": "already_subscribed",
    "STATUS_EMAIL_SENT": "email_sent",
    "STATUS_CONFIRMED": "confirmed",
    "STATUS_LINK_EXPIRED": "link_expired",
    "STATUS_UNSUBSCRIBED": "unsubscribed",
}


@method_decorator(csrf_exempt, name="dispatch")
class SearchView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("query", None)
        page = request.GET.get("page", 1)
        template_path = "patterns/pages/search/search.html"
        context = {}

        # Recruitment site search
        site = Site.find_for_request(request)
        site_is_recruitment = is_recruitment_site(site)
        if site_is_recruitment:
            template_path = "patterns/pages/search/search--jobs.html"
            homepage = Site.find_for_request(request).root_page
            search_results = get_job_search_results(
                querydict=request.GET, homepage=homepage
            )
            if settings.ENABLE_JOBS_SEARCH_ALERT_SUBSCRIPTIONS:
                context["job_alert_form"] = SearchAlertSubscriptionForm
        elif is_blogs_search(request):
            template_path = "patterns/pages/search/search--blogs.html"
            context["blog_parent_page"] = BlogHomePage.objects.get(
                slug=request.GET["parent_page"]
            )
            search_results = get_blogs_search_results(
                search_query, context["blog_parent_page"]
            )

        # Main site search
        else:
            if search_query:
                promotions = (
                    Query.get(search_query)
                    .editors_picks.annotate(
                        section_label=Case(
                            When(
                                page__path__startswith=site.root_page.path,
                                then=Subquery(
                                    Page.objects
                                    # don't self-annotate section indexes
                                    .exclude(pk=OuterRef("page__pk"))
                                    .filter(
                                        depth=3,
                                        path__withinstart=OuterRef("page__path"),
                                    )
                                    .values("title")
                                ),
                            ),
                            default=Subquery(
                                Site.objects.filter(
                                    root_page__path__withinstart=OuterRef("page__path")
                                ).values("site_name")
                            ),
                            output_field=CharField(),
                        )
                    )
                    .all()
                )
                promotion_page_ids = promotions.values_list("page_id", flat=True)

                page_queryset_for_search = (
                    Page.objects.live()
                    .exclude(pk__in=promotion_page_ids)
                    .annotate(
                        section_label=Case(
                            When(
                                path__startswith=site.root_page.path,
                                then=Subquery(
                                    Page.objects
                                    # don't self-annotate section indexes
                                    .exclude(pk=OuterRef("pk"))
                                    .filter(depth=3, path__withinstart=OuterRef("path"))
                                    .values("title")
                                ),
                            ),
                            default=Subquery(
                                Site.objects.filter(
                                    root_page__path__withinstart=OuterRef("path")
                                ).values("site_name")
                            ),
                            output_field=CharField(),
                        )
                    )
                )
                page_queryset_for_search = page_queryset_for_search.not_type(
                    CampaignIndexPage
                )
                page_queryset_for_search = page_queryset_for_search.not_type(
                    CampaignPage
                )

                search_results = page_queryset_for_search.search(
                    search_query, operator="or"
                )

                query = Query.get(search_query)
                # Record hit
                query.add_hit()

                if promotions:
                    search_results = list(chain(promotions, search_results))

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

        search_input_help_text = SystemMessagesSettings.for_site(
            site
        ).search_input_help_text
        no_result_text = SystemMessagesSettings.for_request(
            request
        ).body_no_search_results.format(searchterms=escape(search_query))

        context.update(
            {
                "search_input_help_text": search_input_help_text,
                "no_result_text": no_result_text,
                "search_query": search_query,
                "search_results": search_results,
            }
        )

        if site_is_recruitment:
            context.update(
                {
                    "unfiltered_results": get_job_search_results(
                        querydict=QueryDict("query=" + request.GET.get("query", "")),
                        homepage=homepage,
                    ),
                }
            )

        response = TemplateResponse(
            request,
            template_path,
            context,
        )

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
        site = Site.find_for_request(request)
        if not is_recruitment_site(site):
            return

        form = SearchAlertSubscriptionForm(data=request.POST)

        if form.is_valid():
            # e.g. query=school&category=work-experiencetraineeshipinternship&category=transport-economy-environment
            search = get_current_search(request.GET)
            email = form.cleaned_data["email"]
            context = {"STATUSES": JOB_ALERT_STATUSES}
            homepage = Site.find_for_request(request).root_page.specific

            # Search if already exists and confirmed:
            try:
                subscription = JobAlertSubscription.objects.get(
                    email=email, search=search, homepage=homepage
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
                subscription = JobAlertSubscription(
                    email=email, search=search, homepage=homepage
                )
                subscription.full_clean()
                subscription.save()

            subscription.send_confirmation_email()
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
            request,
            "patterns/pages/jobs_alert/subscription_processed.html",
            context,
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
            request,
            "patterns/pages/jobs_alert/unsubscribe.html",
            context,
        )
        return response
