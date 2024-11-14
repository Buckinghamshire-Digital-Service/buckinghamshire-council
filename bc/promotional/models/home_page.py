from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField

from bc.blogs.models import BlogPostPage
from bc.promotional.blocks.cta import PrimaryMediaWithTextCTA
from bc.utils.models import BasePage

from ..blocks.cards import LinkCards
from ..blocks.explainer import Explainer


class PromotionalHomePage(BasePage):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "promotional.PromotionalSiteConfiguration",
        "promotional.PromotionalContentPage",
        "events.EventIndexPage",
        "blogs.bloghomepage",
    ]
    template = "patterns/pages/promotional/home_page.html"

    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField(max_length=1024, blank=True)
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    hero_link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    hero_link_text = models.CharField(max_length=255)

    teasers = StreamField(
        [
            ("link_cards", LinkCards()),
        ],
        max_num=1,
        blank=True,
    )

    media_with_text_cta = StreamField(
        [("media_with_text_cta", PrimaryMediaWithTextCTA())],
        max_num=1,
        blank=True,
        verbose_name="media with text call to action",
    )

    explainer = StreamField(
        [("explainer", Explainer())],
        max_num=1,
        blank=True,
    )

    recent_blog_posts_title = models.CharField(max_length=255, blank=True)
    recent_blog_posts_page = models.ForeignKey(
        "blogs.BlogHomePage",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        help_text="Select blog home page to which fetch recent blog posts from",
    )
    recent_blog_posts_view_all_link_text = models.CharField(
        max_length=255, blank=True, help_text='Defaults to "View all blogs"'
    )

    search_fields = BasePage.search_fields.copy()
    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            (
                FieldPanel("hero_title"),
                FieldPanel("hero_text"),
                FieldPanel("hero_image"),
                FieldPanel("hero_link_page"),
                FieldPanel("hero_link_text"),
            ),
            heading="Hero",
        ),
        FieldPanel("teasers"),
        FieldPanel("media_with_text_cta"),
        FieldPanel("explainer"),
        MultiFieldPanel(
            (
                FieldPanel("recent_blog_posts_title"),
                FieldPanel("recent_blog_posts_page"),
                FieldPanel("recent_blog_posts_view_all_link_text"),
            ),
            heading="Recent blog posts",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.hero_link_page is not None and self.hero_link_page.live:
            context["hero_link_url"] = self.hero_link_page.get_url(request=request)
        context.update(self.get_recent_blog_posts_context(request=request))
        return context

    def get_recent_blog_posts_context(self, *, request=None):
        if self.recent_blog_posts_page is None or not self.recent_blog_posts_page.live:
            return {}
        qs = (
            BlogPostPage.objects.child_of(self.recent_blog_posts_page)
            .live()
            .prefetch_related("categories", "image__renditions")
            .order_by("-date_published")
        )
        blog_posts = []
        for blog_post in qs[:3]:
            blog_posts.append(
                {
                    "title": blog_post.title,
                    "url": blog_post.get_url(request=request),
                    "published_on": blog_post.date_published,
                    "author": blog_post.author,
                    "image": blog_post.image,
                    "introduction": blog_post.intro_text,
                    "categories": [cat.name for cat in blog_post.categories.all()],
                }
            )
        title = (
            self.recent_blog_posts_title
            or f"Blogs from {self.recent_blog_posts_page.title}"
        )
        view_all_link_text = (
            self.recent_blog_posts_view_all_link_text or "View all blogs"
        )

        return {
            "recent_blog_posts": blog_posts,
            "recent_blog_posts_title": title,
            "recent_blog_posts_view_all_text": view_all_link_text,
            "recent_blog_posts_view_all_url": self.recent_blog_posts_page.get_url(
                request=request
            ),
        }
