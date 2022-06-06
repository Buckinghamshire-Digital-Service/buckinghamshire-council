from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)

from bc.utils.models import BasePage, RelatedPage


class BlogHomePageRelatedPage(RelatedPage):
    source_page = ParentalKey("blogs.BlogHomePage", related_name="related_pages")


class BlogHomePage(BasePage):
    parent_page_types = ["home.homepage"]
    # define subpage types as blogpost page

    template = "patterns/pages/blogs/blog_home_page.html"

    about_title = models.TextField()
    about_description = models.TextField()
    about_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Page link",
    )

    # add featured blogpost page

    # add social media links

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("about_title", heading="Title"),
                FieldPanel("about_description", heading="Description"),
                PageChooserPanel("about_page"),
            ],
            heading="About section",
        ),
        InlinePanel("related_pages", label="Related pages"),
    ]
