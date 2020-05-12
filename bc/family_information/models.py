from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from ..utils.models import BasePage, Orderable

class FamilyInformationHomePage(BasePage):
    template = "patterns/pages/family_information/family_information_home_page.html"

    max_count = 1

    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    call_to_action = models.ForeignKey(
        "utils.CallToActionSnippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    links_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    left_title = models.CharField(max_length=255, null=True)
    left_lede = models.TextField(null=True)
    left_label = models.CharField(max_length=255, null=True, blank=True)
    left_action = models.ForeignKey(
        "wagtailcore.Page", 
        on_delete=models.CASCADE, 
        related_name="+",
        null=True
    )
    right_title = models.CharField(max_length=255, null=True)
    right_lede = models.TextField(null=True)
    right_label = models.CharField(max_length=255, null=True, blank=True)
    right_action = models.ForeignKey(
        "wagtailcore.Page", 
        on_delete=models.CASCADE, 
        related_name="+",
        null=True
    )

    content_panels = BasePage.content_panels + [
        ImageChooserPanel("hero_image"),
        MultiFieldPanel([
                InlinePanel("useful_links", max_num=2, min_num=0, label="Link"),
                ImageChooserPanel("links_image"),
            ],
            heading="Useful links",
        ),
        SnippetChooserPanel("call_to_action"),

        MultiFieldPanel([
            FieldPanel("left_title"),
            FieldPanel("left_lede"),
            FieldPanel("left_label"),
            PageChooserPanel("left_action"),
        ], heading="Left action"),

        MultiFieldPanel([
            FieldPanel("right_title"),
            FieldPanel("right_lede"),
            FieldPanel("right_label"),
            PageChooserPanel("right_action"),
        ], heading="Right action"),
    ]



class UsefulLinks(Orderable):
    page = ParentalKey("family_information.FamilyInformationHomePage", related_name="useful_links")
    title = models.CharField(max_length=255)
    lede = models.TextField()
    url = models.URLField()

    content_panels = [
        FieldPanel("title"),
        FieldPanel("lede"),
        FieldPanel("url"),
    ]