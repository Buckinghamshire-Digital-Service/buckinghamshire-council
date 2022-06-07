from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import models
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

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


class BlogHomePage(SocialMediaLinks, BasePage):
    parent_page_types = ["home.homepage"]
    subpage_types = ["blogs.blogpostpage", "standardpages.informationpage"]

    template = "patterns/pages/blogs/blog_home_page.html"

    about_title = models.TextField()
    about_description = models.TextField()
    about_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Page link",
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
        blogs = BlogPostPage.objects.child_of(self)

        paginator = Paginator(blogs, settings.DEFAULT_PER_PAGE)
        blogs = paginator.get_page(page)

        context = super().get_context(request, *args, **kwargs)
        context.update(
            blogs=blogs,
        )
        return context

    @property
    def featured_image(self):
        if self.featured_blogpost_page:
            if self.featured_blogpost_page.image:
                return self.featured_blogpost_page.image
        return self.featured_blogpost_image

    @property
    def recent_posts(self):
        return BlogPostPage.objects.child_of(self).live().order_by("date_published")[:3]


class BlogPostPage(BasePage):
    parent_page_types = ["blogs.bloghomepage"]

    template = "patterns/pages/blogs/blog_post_page.html"

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
        FieldPanel("intro_text"),
        ImageChooserPanel("image"),
        FieldPanel("author"),
        FieldPanel("date_published"),
        StreamFieldPanel("body"),
    ]

    @cached_property
    def homepage(self):
        return self.get_parent().specific
