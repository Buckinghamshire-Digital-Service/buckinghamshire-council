from django.db import models
from django.db.models import Count, F
from django.shortcuts import get_object_or_404, render

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from bc.utils.constants import RICH_TEXT_FEATURES

from ..utils.models import BasePage


class JobCategory(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def get_categories_summary():
        """Returns a QuerySet that returns dictionaries, when used as an iterable.

           The dictionary keys are: category (category id), count, title, description
           This is ordered by highest count first.
        """
        job_categories = (
            TalentLinkJob.objects.values("category")
            .annotate(id=F("category__id"))
            .annotate(count=Count("category"))
            .annotate(label=F("category__title"))
            .annotate(description=F("category__description"))
            .order_by("-count")
        )
        return job_categories

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Job categories"


class TalentLinkJob(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    last_imported = models.DateTimeField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    talentlink_id = models.IntegerField(unique=True)
    job_number = models.CharField(max_length=10, blank=False)

    title = models.CharField(max_length=255, blank=False)
    short_description = models.TextField()
    description = models.TextField()
    category = models.ForeignKey("recruitment.JobCategory", on_delete=models.PROTECT)
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

    @property
    def url(self):
        homepage = RecruitmentHomePage.objects.live().public().first()
        return homepage.url + homepage.reverse_subpage(
            "job_detail", args=(self.talentlink_id,)
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["job_categories"] = JobCategory.get_categories_summary()

        return context

    @route(r"^job_detail/(\d+)/$")
    def job_detail(self, request, talentlink_id):
        page = get_object_or_404(TalentLinkJob, talentlink_id=talentlink_id)
        return render(request, "patterns/pages/jobs/job_detail.html", {"page": page})
