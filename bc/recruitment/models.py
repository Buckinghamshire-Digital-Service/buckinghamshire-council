import json
import secrets
from urllib.parse import urlsplit, urlunsplit

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, F
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from wagtailorderable.models import Orderable

from bc.utils.email import NotifyEmailMessage

from ..utils.blocks import StoryBlock
from ..utils.constants import RICH_TEXT_FEATURES
from ..utils.models import BasePage


class JobSubcategory(models.Model):
    """
    This corresponds to Job Group in the TalentLink import API
    """

    title = models.CharField(max_length=128)

    def get_categories_list(self):
        if self.categories:
            return list(self.categories.values_list("title", flat=True))

    # Set short description for Modeladmin lists so displays this instead of `get_categories_list`
    get_categories_list.short_description = "Categories"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Job subcategories"
        ordering = ["title"]


class JobCategory(Orderable, models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    subcategories = models.ManyToManyField(JobSubcategory, related_name="categories")
    is_schools_and_early_years = models.BooleanField(default=False)

    slug = models.SlugField(
        allow_unicode=True,
        max_length=255,
        help_text="The name of the category as it will appear in search filter e.g /search/category=[my-slug]",
    )

    def get_subcategories_list(self):
        if self.subcategories:
            return list(self.subcategories.values_list("title", flat=True))

    get_subcategories_list.short_description = "Subcategories"

    @staticmethod
    def get_school_and_early_years_categories():
        return list(
            JobCategory.objects.filter(is_schools_and_early_years=True).values_list(
                "slug", flat=True
            )
        )

    @staticmethod
    def get_categories_summary(queryset=None):
        """Returns a QuerySet that returns dictionaries, when used as an iterable.

           The dictionary keys are: category (category id), count, title, description
           This is ordered by highest count first.
        """
        if not queryset:
            queryset = TalentLinkJob.objects.all()

        job_categories = (
            queryset.annotate(category=F("subcategory__categories"))
            .exclude(category=None)
            .values("category")
            .annotate(key=F("subcategory__categories__slug"))
            .annotate(count=Count("category"))
            .annotate(label=F("subcategory__categories__title"))
            .annotate(description=F("subcategory__categories__description"))
            .annotate(
                is_schools_and_early_years=F(
                    "subcategory__categories__is_schools_and_early_years"
                )
            )
            .annotate(sort_order=F("subcategory__categories__sort_order"))
            .order_by("-count")
        )

        return job_categories

    def _slug_is_available(slug, job_category=None):
        """
        Determine whether the given slug is available for use and not a duplicate
        """
        siblings = JobCategory.objects.all()
        if job_category:
            siblings = siblings.exclude(id=job_category.id)

        return not siblings.filter(slug=slug).exists()

    def get_autogenerated_slug(self):
        base_slug = slugify(self.title)
        if not base_slug:
            return

        candidate_slug = base_slug
        suffix = 1

        while not JobCategory._slug_is_available(candidate_slug, self):
            # try with incrementing suffix until we find a slug which is available
            suffix += 1
            candidate_slug = "%s-%d" % (base_slug, suffix)

        return candidate_slug

    def full_clean(self, *args, **kwargs):
        # Apply fixups that need to happen before per-field validation occurs
        if not self.slug:
            self.slug = self.get_autogenerated_slug()

        super().full_clean(*args, **kwargs)

    def clean(self):
        super().clean()
        if not JobCategory._slug_is_available(self.slug, self):
            raise ValidationError({"slug": "This slug is already in use"})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Job categories"


@receiver(pre_save, sender=JobCategory)
def callback_jobcategory_autogenerate_slug_if_empty(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance.get_autogenerated_slug()


class TalentLinkJob(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    last_imported = models.DateTimeField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    talentlink_id = models.IntegerField(unique=True)
    job_number = models.CharField(max_length=10, blank=False)

    title = models.CharField(max_length=255, blank=False)
    short_description = models.TextField()
    description = models.TextField()
    subcategory = models.ForeignKey(
        "recruitment.JobSubcategory",
        on_delete=models.PROTECT,
        null=True,
        related_name="jobs",
    )
    salary_range = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(max_length=255)
    closing_date = models.DateField()
    expected_start_date = models.DateField(null=True)

    contact_email = models.EmailField()

    searchable_salary = models.CharField(
        max_length=255, help_text="Salary group for filtering"
    )
    searchable_location = models.CharField(max_length=255)
    location_postcode = models.CharField(max_length=8, blank=True)
    location_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    location_lon = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    is_published = models.BooleanField(default=True)
    posting_start_date = models.DateTimeField()
    posting_end_date = models.DateTimeField()
    show_apply_button = models.BooleanField(default=True)
    attachments = models.ManyToManyField(
        "documents.CustomDocument", blank=True, related_name="jobs"
    )
    logo = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    application_url_query = models.CharField(max_length=255)

    def get_categories_list(self):
        if self.subcategory:
            return self.subcategory.get_categories_list()

    # Set short description for Modeladmin lists so displays this instead of `get_categories_list`
    get_categories_list.short_description = "Categories"

    def __str__(self):
        return f"{self.job_number}: {self.title}"

    @cached_property
    def homepage(self):
        return RecruitmentHomePage.objects.live().public().first()

    @property
    def url(self):
        return self.homepage.url + self.homepage.reverse_subpage(
            "job_detail", args=(self.talentlink_id,)
        )

    @property
    def application_url(self):
        base_url = self.homepage.url + self.homepage.reverse_subpage("apply")
        scheme, netloc, path, query, fragment = urlsplit(base_url)
        return urlunsplit((scheme, netloc, path, self.application_url_query, fragment))


@receiver(pre_delete, sender=TalentLinkJob)
def callback_talentlinkjob_delete_attachments_and_logo(
    sender, instance, *args, **kwargs
):
    # if instance.attachments:
    for doc in instance.attachments.all():
        if doc.jobs.all().count() == 1:
            doc.delete()

    # Delete associated logo if it isn't used anywhere else
    if instance.logo and (
        TalentLinkJob.objects.filter(logo=instance.logo).count() == 1
    ):
        instance.logo.delete()


class RecruitmentHomePage(RoutablePageMixin, BasePage):
    template = "patterns/pages/home/home_page--jobs.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    hero_title = models.CharField(
        max_length=255, help_text="e.g. Finding a job in Buckinghamshire"
    )
    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    search_box_placeholder = models.CharField(
        max_length=255, help_text="eg. Search jobs, e.g. “Teacher in Aylesbury”",
    )
    hero_link_text = models.CharField(max_length=255, help_text="e.g. Browse jobs")
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
                FieldPanel("hero_link_text"),
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
        return render(
            request,
            "patterns/pages/jobs/job_detail.html",
            {"page": page, "show_apply_button": page.show_apply_button},
        )

    @route(r"^apply/$")
    def apply(self, request):
        job_id = request.GET.get("jobId")
        if job_id:
            talentlink_id = job_id.split("-")[1]
            page = get_object_or_404(TalentLinkJob, talentlink_id=talentlink_id)
        else:
            raise Http404("Missing job details")
        return render(
            request,
            "patterns/pages/jobs/apply.html",
            {"page": page, "show_apply_button": False},
        )


class RecruitmentIndexPage(BasePage):
    template = "patterns/pages/standardpages/index_page--jobs.html"

    hero_image = models.ForeignKey(
        "images.CustomImage", null=True, related_name="+", on_delete=models.SET_NULL,
    )
    body = StreamField(StoryBlock(required=False), blank=True)

    content_panels = BasePage.content_panels + [
        ImageChooserPanel("hero_image"),
        StreamFieldPanel("body"),
    ]

    @cached_property
    def child_pages(self):
        return self.get_children().live().public().specific().order_by("path")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["subpages"] = self.child_pages

        return context


class JobAlertSubscription(models.Model):
    email = models.EmailField()
    search = models.TextField(
        default="{}", editable=False
    )  # stop site admins from entering bad values
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, unique=True, editable=False)

    @property
    def confirmation_url(self):
        return reverse("confirm_job_alert", args=[self.token])

    @property
    def unsubscribe_url(self):
        return reverse("unsubscribe_job_alert", args=[self.token])

    def full_clean(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)

        super().full_clean(*args, **kwargs)

    def send_confirmation_email(self, request):
        template_name = "patterns/email/confirm_job_alert.txt"
        context = {}
        context["search"] = json.loads(self.search)
        context["confirmation_url"] = request.build_absolute_uri(self.confirmation_url)
        context["unsubscribe_url"] = request.build_absolute_uri(self.unsubscribe_url)

        content = render_to_string(template_name, context=context)
        email = NotifyEmailMessage(
            subject="Job alert subscription", body=content, to=[self.email]
        )
        email.send()


@receiver(pre_save, sender=JobAlertSubscription)
def callback_jobalertsubscription_run_full_clean(sender, instance, *args, **kwargs):
    if not instance.token:
        instance.full_clean()


class JobAlertNotificationTask(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True)
    is_successful = models.BooleanField(default=False)
