import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail import models as wt_models
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField

from django_gov_notify.message import NotifyEmailMessage

from bc.blogs.forms import BlogHomePageForm, BlogPostPageForm
from bc.utils.blocks import StoryBlock
from bc.utils.constants import ALERT_SUBSCRIPTION_STATUSES
from bc.utils.models import BasePage, RelatedPage
from bc.utils.validators import (
    validate_facebook_domain,
    validate_linkedin_domain,
    validate_youtube_domain,
)


class BlogHomePageRelatedPage(RelatedPage):
    source_page = ParentalKey("blogs.BlogHomePage", related_name="related_pages")


class SocialMediaLinks(models.Model):
    twitter_handle = models.CharField(
        max_length=255,
        blank=True,
        help_text="The Twitter username without the @, e.g. katyperry",
    )
    facebook_page_url = models.CharField(
        max_length=255, blank=True, validators=[validate_facebook_domain]
    )
    youtube_channel_url = models.URLField(
        blank=True,
        validators=[validate_youtube_domain],
    )
    linkedin_url = models.CharField(
        max_length=255,
        blank=True,
        validators=[validate_linkedin_domain],
    )

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_handle"),
                FieldPanel("facebook_page_url"),
                FieldPanel("youtube_channel_url", heading="YouTube channel URL"),
                FieldPanel(
                    "linkedin_url",
                    heading="LinkedIn URL",
                ),
            ],
            heading="Social media URLs",
        )
    ]

    class Meta:
        abstract = True

    def has_any_social_setting(self):
        return any(
            [
                self.twitter_handle,
                self.facebook_page_url,
                self.youtube_channel_url,
                self.linkedin_url,
            ]
        )

    @property
    def socials(self):
        return {
            "twitter_handle": self.twitter_handle,
            "facebook_page_url": self.facebook_page_url,
            "youtube_channel_url": self.youtube_channel_url,
            "linkedin_url": self.linkedin_url,
        }


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(editable=False)

    panels = [FieldPanel("name")]

    class Meta:
        abstract = True
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class BlogHomePageCategories(wt_models.Orderable, Category):
    page = ParentalKey(
        "blogs.BlogHomePage",
        on_delete=models.CASCADE,
        related_name="blog_categories",
    )

    class Meta(Category.Meta):
        constraints = [
            models.UniqueConstraint(fields=["page", "slug"], name="unique_page_slug"),
        ]

    @cached_property
    def url(self):
        return self.page.category_url(self.slug)

    def clean(self):
        self.slug = slugify(self.name)
        super().clean()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.full_clean()
        self.validate_unique()
        super().save(*args, *kwargs)


class BlogHomePage(RoutablePageMixin, SocialMediaLinks, BasePage):
    base_form_class = BlogHomePageForm

    parent_page_types = ["blogs.blogglobalhomepage"]
    subpage_types = ["blogs.blogpostpage", "blogs.blogaboutpage"]

    template = "patterns/pages/blogs/blog_home_page.html"

    about_title = models.TextField()
    about_description = models.TextField()
    about_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Page link",
        null=True,
        blank=True,
    )

    featured_blogpost_page = models.ForeignKey(
        "blogs.blogpostpage",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="Page link",
    )
    featured_blogpost_image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        help_text="If the page has its own image, it will override any image set here.",
    )

    content_panels = (
        BasePage.content_panels
        + [
            MultiFieldPanel(
                [
                    FieldPanel("about_title", heading="Title"),
                    FieldPanel("about_description", heading="Description"),
                    PageChooserPanel("about_page", page_type="blogs.blogaboutpage"),
                ],
                heading="About section",
            ),
            InlinePanel(
                "blog_categories", heading="Categories", label="Category", min_num=1
            ),
            MultiFieldPanel(
                [
                    FieldPanel("featured_blogpost_page"),
                    FieldPanel("featured_blogpost_image", heading="Image"),
                ],
                heading="Featured blogpost",
            ),
            InlinePanel("related_pages", label="Related pages"),
        ]
        + SocialMediaLinks.content_panels
    )

    def clean(self):
        super().clean()
        if self.featured_blogpost_page and not (
            self.featured_blogpost_page.image or self.featured_blogpost_image
        ):
            raise ValidationError(
                {
                    "featured_blogpost_image": "Featured blog post has no image. Please select a custom image."
                }
            )

    def get_context(self, request, *args, **kwargs):
        page = request.GET.get("page", 1)
        blogs = BlogPostPage.objects.child_of(self).live().order_by("-date_published")

        paginator = Paginator(blogs, settings.DEFAULT_PER_PAGE)
        blogs = paginator.get_page(page)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            blogs=blogs,
        )
        return context

    @property
    def featured_image(self):
        if self.featured_blogpost_image:
            return self.featured_blogpost_image
        return self.featured_blogpost_page.image

    @property
    def categories(self):
        categories = (
            self.blog_categories.annotate(
                num_related_posts=models.Count("related_posts")
            )
            .filter(num_related_posts__gt=0)
            .values("name", "num_related_posts", "slug")
        )
        for category in categories:
            category["url"] = self.category_url(category=category["slug"])
        return categories

    @property
    def recent_posts(self):
        return (
            BlogPostPage.objects.child_of(self).live().order_by("-date_published")[:3]
        )

    @route(r"^search/$", name="blog-search")
    def search(self, request):
        from bc.blogs.views import SearchView

        return SearchView.as_view()(request, blog_home_page=self)

    @route(r"^category/(?P<category>[\w-]+)/$", name="blog-category")
    def category(self, request, category):
        from bc.blogs.views import CategoryView

        return CategoryView.as_view()(request, blog_home_page=self, category=category)

    @property
    def search_url(self):
        return self.url + self.reverse_subpage("blog-search")

    def category_url(self, category):
        return self.url + self.reverse_subpage("blog-category", args=[category])

    @route(r"^subscribe-to-alert/$", name="subscribe_to_alert")
    def subscribe_to_alert(self, request):
        from bc.blogs.views import BlogSubscribeView

        return BlogSubscribeView.as_view()(request, blog_home_page=self)

    @route(
        r"^manage-subscription/(?P<token>[a-zA-Z0-9_-]+)/$", name="manage_subscription"
    )
    def manage_subscription(self, request, token):
        from bc.blogs.views import BlogManageSubscribeView

        return BlogManageSubscribeView.as_view()(
            request, blog_home_page=self, token=token
        )

    @route(
        r"^confirm-blog-alert/(?P<token>[a-zA-Z0-9_-]+)/$", name="confirm_blog_alert"
    )
    def confirm_blog_alert(self, request, token):
        from bc.blogs.views import BlogAlertConfirmView

        return BlogAlertConfirmView.as_view()(request, blog_home_page=self, token=token)

    @route(r"^confirmation_mail_alert/$", name="confirmation_mail_alert")
    def confirmation_mail_alert(self, request):
        return TemplateView.as_view(
            template_name="patterns/pages/blogs/subscribe/subscribe_page_confirm.html",
            extra_context={
                "status": ALERT_SUBSCRIPTION_STATUSES["STATUS_EMAIL_SENT"],
                "STATUSES": ALERT_SUBSCRIPTION_STATUSES,
                "page": self,
            },
        )(request)

    @property
    def subscribe_to_alert_url(self):
        return self.url + self.reverse_subpage("subscribe_to_alert")

    @property
    def confirmation_mail_alert_url(self):
        return self.url + self.reverse_subpage("confirmation_mail_alert")

    def manage_subscription_alert_url(self, token):
        return self.full_url + self.reverse_subpage("manage_subscription", args=[token])

    def alert_confirmation_full_url(self, token):
        return self.full_url + self.reverse_subpage("confirm_blog_alert", args=[token])


class BlogAboutPage(BasePage):
    parent_page_types = ["blogs.bloghomepage"]
    max_count_per_parent = 1

    template = "patterns/pages/blogs/blog_about_page.html"

    intro_text = models.TextField()

    image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    body = StreamField(StoryBlock(), use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("intro_text"),
        FieldPanel("image"),
        FieldPanel("body"),
    ]

    @cached_property
    def homepage(self):
        return self.get_parent().specific


class BlogPostPage(BasePage):
    parent_page_types = ["blogs.bloghomepage"]
    base_form_class = BlogPostPageForm

    template = "patterns/pages/blogs/blog_post_page.html"

    categories = ParentalManyToManyField(
        "blogs.BlogHomePageCategories", related_name="related_posts"
    )

    intro_text = models.TextField()

    image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    author = models.TextField()
    date_published = models.DateField()

    body = StreamField(StoryBlock(), use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("categories", widget=CheckboxSelectMultiple),
        FieldPanel("intro_text"),
        FieldPanel("image"),
        FieldPanel("author"),
        FieldPanel("date_published"),
        FieldPanel("body"),
    ]

    @cached_property
    def homepage(self):
        return self.get_parent().specific


class BlogGlobalHomePage(BasePage):
    parent_page_types = ["home.homepage"]
    subpage_types = ["blogs.bloghomepage"]
    max_count = 1
    template = "patterns/pages/blogs/blog_global_home_page.html"

    @property
    def blog_home_pages(self):
        return BlogHomePage.objects.child_of(self).live().order_by("path")

    @property
    def recent_posts(self):
        return (
            BlogPostPage.objects.descendant_of(self)
            .live()
            .order_by("-date_published")[:3]
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog_home_pages"] = self.blog_home_pages
        context["recent_posts"] = self.recent_posts

        return context


class BlogAlertSubscription(models.Model):
    email = models.EmailField()
    homepage = models.ForeignKey(
        "BlogHomePage", on_delete=models.CASCADE, blank=True, null=True
    )
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, unique=True, editable=False)

    def full_clean(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)

        super().full_clean(*args, **kwargs)

    @property
    def confirmation_url(self):
        return self.homepage.alert_confirmation_full_url(self.token)

    @property
    def manage_url(self):
        return self.homepage.manage_subscription_alert_url(self.token)

    def get_email_context(self):
        return {
            "confirmation_url": self.confirmation_url,
            "manage_url": self.manage_url,
            "homepage": self.homepage,
        }

    def send_confirmation_email(self):
        template_name = "patterns/email/confirm_blog_alert.txt"
        context = self.get_email_context()
        content = render_to_string(template_name, context=context)
        email = NotifyEmailMessage(
            subject="Blog alert subscription", body=content, to=[self.email]
        )
        email.send()


class NotificationRecord(models.Model):
    was_sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    blog_post = models.ForeignKey(
        "BlogPostPage",
        on_delete=models.CASCADE,
        related_name="+",
    )
