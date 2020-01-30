from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import Truncator

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from bc.utils.constants import RICH_TEXT_FEATURES

from ..utils.models import BasePage


class TalentLinkJob(models.Model):

    talentlink_id = models.IntegerField(unique=True)
    job_number = models.CharField(max_length=10, unique=True, blank=False)

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    category = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=255)
    closing_date = models.DateField()
    expected_start_date = models.DateField(null=True)

    contact_email = models.EmailField()

    searchable_salary = models.CharField(
        max_length=255, help_text="Salary group for filtering"
    )
    searchable_location = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
    posting_start_date = models.DateTimeField()
    posting_end_date = models.DateTimeField()
    show_apply_button = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_number}: {self.title}"

    @cached_property
    def short_description(self):
        if self.description:
            # Imported description typically start with a 'Overview' heading which we want to remove.
            clean_description = strip_tags(
                self.description.replace("<h2>Overview</h2>", "", 1)
            )
            return Truncator(clean_description).chars(140)

    @property
    def url(self):
        homepage = RecruitmentHomePage.objects.live().public().first()
        return homepage.url + homepage.reverse_subpage(
            "job_detail", args=(self.job_number,)
        )


class RecruitmentHomePage(RoutablePageMixin, BasePage):
    template = "patterns/pages/home/home_page--jobs.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    hero_title = models.CharField(
        max_length=255, help_text="eg. Finding a job in Buckinghamshire"
    )
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    search_box_placeholder = models.CharField(
        max_length=255, help_text="eg. Search jobs, e.g. “Teacher in Aylesbury”",
    )
    body = StreamField(
        blocks.StreamBlock(
            [
                (
                    "content_block",
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock()),
                            (
                                "paragraph",
                                blocks.RichTextBlock(features=RICH_TEXT_FEATURES),
                            ),
                        ],
                        icon="list-ul",
                    ),
                )
            ],
            max_num=2,
            required=False,
        ),
        blank=True,
    )
    search_fields = BasePage.search_fields + [index.SearchField("hero_title")]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                ImageChooserPanel("hero_image"),
                FieldPanel("search_box_placeholder"),
            ],
            "Hero",
        ),
        StreamFieldPanel("body"),
    ]

    @route(r"^job_detail/(\w+)/$")
    def job_detail(self, request, job_number):
        page = get_object_or_404(TalentLinkJob, job_number=job_number)
        return render(request, "patterns/pages/jobs/job_detail.html", {"page": page})
