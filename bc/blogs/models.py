from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import models as wt_models
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from bc.blogs.forms import BlogHomePageForm, BlogPostPageForm
from bc.utils.blocks import StoryBlock
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
        related_name="related_categories",
    )

    class Meta(Category.Meta):
        constraints = [
            models.UniqueConstraint(fields=["page", "slug"], name="unique_page_slug"),
        ]

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
    subpage_types = ["blogs.blogpostpage", "standardpages.informationpage"]

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
                    PageChooserPanel(
                        "about_page", page_type="standardpages.informationpage"
                    ),
                ],
                heading="About section",
            ),
            InlinePanel(
                "related_categories", heading="Categories", label="Category", min_num=1
            ),
            MultiFieldPanel(
                [
                    PageChooserPanel("featured_blogpost_page"),
                    ImageChooserPanel("featured_blogpost_image", heading="Image"),
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
        blogs = BlogPostPage.objects.child_of(self).order_by("-date_published")

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
        return self.related_categories.annotate(
            num_related_posts=models.Count("related_posts")
        ).values("name", "num_related_posts")

    @property
    def recent_posts(self):
        return (
            BlogPostPage.objects.child_of(self).live().order_by("-date_published")[:3]
        )

    @route(r"^search/$", name="blog-search")
    def search(self, request):
        from bc.blogs.views import SearchView

        return SearchView.as_view()(request, blog_home_page=self)

    @property
    def search_url(self):
        return self.url + self.reverse_subpage("blog-search")


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

    body = StreamField(StoryBlock())

    content_panels = BasePage.content_panels + [
        FieldPanel("categories", widget=CheckboxSelectMultiple),
        FieldPanel("intro_text"),
        ImageChooserPanel("image"),
        FieldPanel("author"),
        FieldPanel("date_published"),
        StreamFieldPanel("body"),
    ]

    @cached_property
    def homepage(self):
        return self.get_parent().specific


class BlogGlobalHomePage(BasePage):
    parent_page_types = ["home.homepage"]
    subpage_types = ["blogs.bloghomepage"]
    max_count = 1

    def serve(self, request, *args, **kwargs):
        site = wt_models.Site.find_for_request(request)
        return redirect(site.root_page.url)
