from django.contrib.postgres.fields import ArrayField
from django.db import models

from wagtail.admin.panels import FieldPanel


class Term(models.Model):
    canonical_term = models.CharField(
        max_length=50,
        unique=True,
        help_text="A word or phrase that returns intended search results",
    )
    synonyms = ArrayField(
        models.CharField(max_length=50, blank=False),
        help_text=(
            "A list of other terms which should match pages containing the canonical "
            "term. Separate with commas, multiple word phrases are supported."
        ),
    )

    panels = [
        FieldPanel("canonical_term"),
        FieldPanel("synonyms"),
    ]

    class Meta:
        verbose_name = "Search synonym"

    def __str__(self):
        synonyms = ", ".join(self.synonyms[:5])
        return f"{self.canonical_term}: {synonyms}"
