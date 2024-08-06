from django.db import models
from django.utils.html import format_html

from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.search import index


class ServiceDirectoryQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(is_enabled=True)


class ServiceDirectory(index.Indexed, models.Model):
    FRONTEND_URL_HELP_TEXT = (
        "The URL for users use to access the directory interface, "
        'for example: "https://directory.familyinfo.buckinghamshire.gov.uk/". '
        "This is used to generate links to the directory services"
    )
    DIRECTORY_API_URL_HELP_TEXT = (
        "The URL of the specific directory API is available at, "
        'for example: "https://api.familyinfo.buckinghamshire.gov.uk/api/v1"'
    )
    MANAGEMENT_API_URL_HELP_TEXT = (
        "The URL of the directory management API is available at, for example: "
        '"https://manage-directory-listing.buckinghamshire.gov.uk/api/v1"'
    )

    is_enabled = models.BooleanField(default=True)
    frontend_url = models.URLField(
        verbose_name="frontend interface URL", help_text=FRONTEND_URL_HELP_TEXT
    )
    admin_name = models.CharField(max_length=128)
    directory_api_url = models.URLField(
        verbose_name="directory API URL",
        help_text=DIRECTORY_API_URL_HELP_TEXT,
    )
    directory_api_slug = models.CharField(
        max_length=255,
        verbose_name="directory API slug",
        help_text='Slug used to identify this directory in the directory API, for example: "bfis"',
    )
    management_api_url = models.URLField(
        verbose_name="management API URL", help_text=MANAGEMENT_API_URL_HELP_TEXT
    )
    objects = ServiceDirectoryQuerySet.as_manager()

    panels = [
        FieldPanel("admin_name"),
        FieldPanel("is_enabled"),
        FieldPanel("frontend_url"),
        MultiFieldPanel(
            [
                FieldPanel("directory_api_url"),
                FieldPanel("directory_api_slug"),
            ],
            heading="Directory API",
        ),
        FieldPanel("management_api_url"),
    ]

    search_fields = [
        index.SearchField("admin_name"),
        index.AutocompleteField("admin_name"),
        index.FilterField("is_enabled"),
        index.SearchField("directory_api_slug"),
        index.AutocompleteField("directory_api_slug"),
    ]

    class Meta:
        verbose_name_plural = "service directories"

    def __str__(self) -> str:
        return self.admin_name


class Taxonomy(index.Indexed, models.Model):
    HELP_PANEL_HTML = format_html(
        "<strong>{}</strong>",
        "Do not edit these values as they come from the API! This is enabled for debugging purposes only.",
    )
    fetched_with_directory = models.ForeignKey(
        ServiceDirectory, on_delete=models.CASCADE, related_name="taxonomies"
    )
    label = models.CharField(max_length=255)
    level = models.IntegerField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child_taxonomies", null=True
    )
    remote_id = models.BigIntegerField(verbose_name="remote ID")
    remote_slug = models.CharField(max_length=255)

    search_fields = [
        index.SearchField("label"),
        index.AutocompleteField("label"),
        index.SearchField("remote_slug"),
        index.AutocompleteField("remote_slug"),
        index.RelatedFields(
            "fetched_with_directory",
            [
                index.SearchField("admin_name"),
                index.AutocompleteField("admin_name"),
            ],
        ),
        index.FilterField("fetched_with_directory"),
        index.FilterField("level"),
    ]

    panels = [
        HelpPanel(HELP_PANEL_HTML),
        FieldPanel("label"),
        FieldPanel("level"),
        FieldPanel("parent"),
        FieldPanel("remote_id"),
        FieldPanel("remote_slug"),
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fetched_with_directory", "remote_id"],
                name="unique_remote_id_per_directory",
            ),
        ]
        verbose_name = "service directory taxonomy"
        verbose_name_plural = "service directory taxonomies"

    def __str__(self) -> str:
        return f"{self.label} ({self.fetched_with_directory})"
