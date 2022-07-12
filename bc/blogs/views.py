from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.timezone import now
from django.views import View
from django.views.generic import FormView, ListView

from bc.blogs.forms import BlogAlertSubscriptionForm, BlogSubscriptionManageForm
from bc.blogs.models import BlogAlertSubscription, BlogHomePageCategories
from bc.blogs.utils import get_blogs_search_results
from bc.utils.constants import ALERT_SUBSCRIPTION_STATUSES


class BlogListView(ListView):
    paginate_by = settings.DEFAULT_PER_PAGE

    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs[self.page_kwarg] = "last"
            return super().paginate_queryset(queryset, page_size)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "page": self.blog_home_page,
        }

    def get(self, request, blog_home_page):
        self.blog_home_page = blog_home_page
        return super().get(request, blog_home_page)


class SearchView(BlogListView):
    template_name = "patterns/pages/blogs/blog_search_listing.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "search_query": self.search_query,
        }

    def get(self, request, blog_home_page):
        self.search_query = request.GET.get("query", None)
        return super().get(request, blog_home_page)

    def get_queryset(self):
        return get_blogs_search_results(self.search_query, self.blog_home_page)


class CategoryView(BlogListView):
    template_name = "patterns/pages/blogs/blog_category_listing.html"

    def get(self, request, blog_home_page, category):
        self.category = BlogHomePageCategories.objects.get(
            slug=category, page=blog_home_page
        )
        return super().get(request, blog_home_page)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "category": self.category,
        }

    def get_queryset(self):
        return self.category.related_posts.live().order_by("-date_published")


class BlogSubscribeView(FormView):
    form_class = BlogAlertSubscriptionForm
    template_name = "patterns/pages/blogs/subscribe/subscribe_page.html"

    def get(self, request, blog_home_page):
        return self.render_to_response(
            self.get_context_data(blog_home_page=blog_home_page)
        )

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "page": kwargs["blog_home_page"]}

    def post(self, request, blog_home_page):
        self.blog_home_page = blog_home_page
        return super().post(request, blog_home_page)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            subscription = BlogAlertSubscription.objects.get(
                email=email, homepage=self.blog_home_page
            )
            if subscription.confirmed:
                return super().form_valid(form)
            else:
                # Treat this as a new subscription request
                subscription.created = now()

        except BlogAlertSubscription.DoesNotExist:
            subscription = BlogAlertSubscription(
                email=email, homepage=self.blog_home_page
            )
            subscription.full_clean()
            subscription.save()

        subscription.send_confirmation_email()
        return super().form_valid(form)

    def get_success_url(self):
        return self.blog_home_page.confirmation_mail_alert_url


class BlogAlertConfirmView(View):
    def get(self, request, blog_home_page, token):
        context = {"STATUSES": ALERT_SUBSCRIPTION_STATUSES, "page": blog_home_page}

        try:
            subscription = BlogAlertSubscription.objects.get(token=token)
        except BlogAlertSubscription.DoesNotExist:
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
                    "title": "Blog alert subscription confirmed",
                    "status": context["STATUSES"]["STATUS_CONFIRMED"],
                }
            )

        response = TemplateResponse(
            request,
            "patterns/pages/blogs/subscribe/subscribe_page_confirm.html",
            context,
        )
        return response


class BlogAlertUnsubscribeView(View):
    def get(self, request, blog_home_page, token):
        context = {"STATUSES": ALERT_SUBSCRIPTION_STATUSES, "page": blog_home_page}

        try:
            subscription = BlogAlertSubscription.objects.get(token=token)
        except BlogAlertSubscription.DoesNotExist:
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
                    "title": "Blog alert unsubscribed",
                    "status": context["STATUSES"]["STATUS_UNSUBSCRIBED"],
                }
            )

        response = TemplateResponse(
            request,
            "patterns/pages/blogs/subscribe/subscribe_page_confirm.html",
            context,
        )
        return response


class BlogManageSubscribeView(FormView):
    form_class = BlogSubscriptionManageForm
    template_name = "patterns/pages/blogs/subscribe/subscribe_page_manage.html"

    def get(self, request, blog_home_page, token):
        subscription = get_object_or_404(BlogAlertSubscription, token=token)
        return self.render_to_response(
            {
                **self.get_context_data(),
                "subscription": subscription,
                "page": blog_home_page,
            }
        )

    def get_initial(self):
        return {
            **super().get_initial(),
            "subscribe": True,  # since self.subscription didn't raise 404, subscription must exist,
            # because while unsubscribing, record is deleted from db
        }

    def post(self, request, blog_home_page, token):
        self.subscription = get_object_or_404(BlogAlertSubscription, token=token)
        self.blog_home_page = blog_home_page
        return super().post(request, blog_home_page)

    def get_success_url(self):
        return self.blog_home_page.manage_subscription_alert_url(
            self.subscription.token
        )

    def form_valid(self, form):
        subscribe = form.cleaned_data["subscribe"]
        if subscribe == "False":
            self.subscription.delete()
            return redirect(self.blog_home_page.full_url)
        return super().form_valid(form)
