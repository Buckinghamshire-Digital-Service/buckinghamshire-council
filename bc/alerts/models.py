from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField

from bc.utils.constants import RICH_PARAGRAPH_FEATURES


class Alert(models.Model):
    PAGE_ONLY = "page only"
    PAGE_AND_DESCENDANTS = "descendants"
    SHOW_ON_CHOICES = (
        (PAGE_ONLY, "the selected page only"),
        (PAGE_AND_DESCENDANTS, "the selected page and all pages below it"),
    )

    title = models.CharField(max_length=255)
    content = RichTextField(
        blank=True, max_length=255, features=RICH_PARAGRAPH_FEATURES
    )
    show_on = models.CharField(
        max_length=20,
        verbose_name="Show on",
        default=PAGE_AND_DESCENDANTS,
        choices=SHOW_ON_CHOICES,
    )
    page = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.CASCADE, related_name="alerts"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("content"),
        MultiFieldPanel(
            [
                PageChooserPanel("page"),
                FieldPanel(
                    "show_on",
                    widget=forms.RadioSelect(attrs={"class": "no-float"}),
                    classname="no-float",
                ),
            ],
            "behaviour",
        ),
    ]

    def __str__(self):
        return self.title
