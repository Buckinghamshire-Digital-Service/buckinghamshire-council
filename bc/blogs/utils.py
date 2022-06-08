from bc.blogs.models import BlogPostPage


def get_blogs_search_results(search_query, homepage):
    if search_query:
        queryset = BlogPostPage.objects.live().child_of(homepage)
        search_results = queryset.search(search_query, operator="or")
    else:
        search_results = BlogPostPage.objects.none()
    return search_results
