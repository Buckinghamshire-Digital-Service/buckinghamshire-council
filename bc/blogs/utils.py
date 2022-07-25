from django.template.loader import render_to_string

from django_gov_notify.message import NotifyEmailMessage

from bc.blogs.models import BlogAlertSubscription, BlogHomePage, BlogPostPage


def get_blogs_search_results(search_query, homepage):
    if search_query:
        queryset = BlogPostPage.objects.live().child_of(homepage)
        search_results = queryset.search(search_query, operator="or")
    else:
        search_results = BlogPostPage.objects.none()
    return search_results


def alert_subscribed_users(blog_post_page_pk):
    blog_post_page = BlogPostPage.objects.get(pk=blog_post_page_pk)
    blog_home_page = BlogHomePage.objects.parent_of(blog_post_page).first()
    subscriptions = BlogAlertSubscription.objects.filter(
        confirmed=True, homepage=blog_home_page
    )

    emails = []
    subject = f"New blog from { blog_home_page.title }"

    context = {"blog_post_page": blog_post_page, "blog_home_page": blog_home_page}

    for subscription in subscriptions:
        content = render_to_string(
            "patterns/email/new_blog_alert.txt",
            context={**context, "alert_manage_url": subscription.manage_url},
        )
        emails.append(
            NotifyEmailMessage(subject=subject, body=content, to=[subscription.email])
        )

    for email in emails:
        email.send()
