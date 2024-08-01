from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from bs4 import BeautifulSoup

from bc.utils.constants import RICH_PARAGRAPH_FEATURES


class Alert(models.Model):
    PAGE_ONLY = "page only"
    PAGE_AND_DESCENDANTS = "descendants"
    SHOW_ON_CHOICES = (
        (PAGE_ONLY, "the selected page only"),
        (PAGE_AND_DESCENDANTS, "the selected page and all pages below it"),
    )

    HIGH = 1
    MEDIUM = 2
    LOW = 3
    LEVEL_CHOICES = (
        (HIGH, "Alert 1"),
        (MEDIUM, "Alert 2"),
        (LOW, "Alert 3"),
    )
    LEVEL_CLASSES = {
        HIGH: "black",
        MEDIUM: "orange",
        LOW: "blue",
    }

    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, features=RICH_PARAGRAPH_FEATURES)
    # Allows negative values in case we get an alert level lower than the default
    alert_level = models.SmallIntegerField(
        choices=LEVEL_CHOICES,
        default=MEDIUM,
        help_text="With Alert 1 as the highest alert",
    )
    show_on = models.CharField(
        max_length=20,
        verbose_name="Show on",
        default=PAGE_AND_DESCENDANTS,
        choices=SHOW_ON_CHOICES,
    )
    page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        related_name="alerts",
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("content"),
        FieldPanel("alert_level"),
        MultiFieldPanel(
            [
                FieldPanel("page"),
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

    def get_alert_level_class(self):
        return self.LEVEL_CLASSES[self.alert_level]

    @classmethod
    def get_alerts_for_page(cls, page):
        if not isinstance(page, Page):
            return cls.objects.none()
        return cls.objects.filter(
            models.Q(page__in=page.get_ancestors(), show_on=cls.PAGE_AND_DESCENDANTS)
            | models.Q(page=page)
        ).order_by("alert_level", "page__path")[:3]

    def clean(self):
        super().clean()

        content = BeautifulSoup(self.content, "html.parser")

        if len(content.text) > 255:
            raise ValidationError(
                {"content": "Text of content can be up to 255 characters"}
            )
