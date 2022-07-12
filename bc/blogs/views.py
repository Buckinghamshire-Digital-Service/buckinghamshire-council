from django.conf import settings
from django.http import Http404
from django.views.generic import ListView

from bc.blogs.models import RelatedCategories
from bc.blogs.utils import get_blogs_search_results


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
        self.category = RelatedCategories.objects.get(
            slug=category, source_page=blog_home_page
        )
        return super().get(request, blog_home_page)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "category": self.category,
        }

    def get_queryset(self):
        return self.category.related_posts.live()
