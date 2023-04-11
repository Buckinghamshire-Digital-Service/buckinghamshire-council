import json
import secrets
from datetime import date
from urllib.parse import urlsplit, urlunsplit

from django import forms
from django.conf import settings
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
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from django_gov_notify.message import NotifyEmailMessage
from wagtailorderable.models import Orderable

from bc.utils.choices import IconChoice

from ..utils.blocks import StoryBlock
from ..utils.constants import RICH_TEXT_FEATURES
from ..utils.models import BasePage
from .blocks import AwardBlock, JobPlatformBlock, MediaBlock
from .constants import JOB_BOARD_CHOICES
from .text_utils import extract_salary_range


class JobSubcategory(models.Model):
    """
    This corresponds to Job Group in the TalentLink import API
    """

    title = models.CharField(max_length=128, unique=True)

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
    icon = models.CharField(
        max_length=20,
        blank=True,
        choices=IconChoice.choices,
    )
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
    def get_categories_summary(queryset=None, homepage=None):
        """
        Returns a QuerySet that returns dictionaries, when used as an iterable.

        The dictionary keys are: category (category id), count, title, description
        This is ordered by highest count first.
        """
        if not homepage:
            homepage = RecruitmentHomePage.objects.live().first()
        if not queryset:
            queryset = TalentLinkJob.objects.filter(homepage=homepage).all()
        else:
            queryset = queryset.filter(homepage=homepage)

        job_categories = (
            queryset.annotate(category=F("subcategory__categories"))
            .exclude(category=None)
            .values("category")
            .annotate(key=F("subcategory__categories__slug"))
            .annotate(icon=F("subcategory__categories__icon"))
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
    last_modified = models.DateTimeField(
        auto_now=True
    )  # For debugging; not modified during normal application flow.

    talentlink_id = models.IntegerField(unique=True)
    job_number = models.CharField(max_length=10, blank=False)
    homepage = models.ForeignKey(
        "RecruitmentHomePage", on_delete=models.CASCADE, blank=True, null=True
    )
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
    dbs_check = models.TextField(
        default="No", verbose_name="Does the role require a DBS check?"
    )
    closing_date = models.DateField()
    expected_start_date = models.DateField(null=True)
    interview_date = models.DateField(null=True)

    contact_email = models.EmailField()

    searchable_salary = models.CharField(
        max_length=255, help_text="Salary group for filtering"
    )
    location_name = models.CharField(max_length=255)
    location_street_number = models.CharField(max_length=32, blank=True)
    location_street = models.CharField(max_length=255, blank=True)
    location_city = models.CharField(max_length=32, blank=True)
    location_region = models.CharField(max_length=32, blank=True)
    location_country = models.CharField(max_length=32, blank=True)
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
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    application_url_query = models.CharField(max_length=255)
    organisation = models.TextField(blank=True)

    def get_categories_list(self):
        if self.subcategory:
            return self.subcategory.get_categories_list()

    # Set short description for Modeladmin lists so displays this instead of `get_categories_list`
    get_categories_list.short_description = "Categories"

    def __str__(self):
        return f"{self.job_number}: {self.title}"

    @property
    def url(self):
        return self.homepage.url + self.homepage.reverse_subpage(
            "job_detail", args=(self.talentlink_id,)
        )

    @property
    def application_url(self):
        """Returns the full application URL including hostname"""
        base_url = self.homepage.full_url + self.homepage.reverse_subpage("apply")
        scheme, netloc, path, query, fragment = urlsplit(base_url)
        return urlunsplit((scheme, netloc, path, self.application_url_query, fragment))

    def full_clean(self, *args, **kwargs):
        if not self.homepage:
            self.homepage = RecruitmentHomePage.objects.live().first()

        super().full_clean(*args, **kwargs)

    @property
    def schema_org_markup(self):
        markup = {
            "@context": "http://schema.org",
            "@type": "JobPosting",
            "datePosted": self.posting_start_date.isoformat(),
            "description": self.short_description,
            "title": self.title,
            "validThrough": self.closing_date.isoformat(),
            "employmentType": self.working_hours,
            "hiringOrganization": {"@type": "Organization", "name": self.organisation},
            "identifier": {
                "@type": "PropertyValue",
                "name": "Reference Number",
                "value": self.job_number,
            },
            "jobLocation": {
                "@type": "Place",
                "name": self.location_name,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": " ".join(
                        [self.location_street_number, self.location_street]
                    ),
                    "addressLocality": self.location_city,
                    "addressRegion": self.location_region,
                    "postalCode": self.location_postcode,
                    "addressCountry": self.location_country,
                },
            },
        }

        if self.logo:
            markup["hiringOrganization"]["logo"] = self.logo.get_rendition(
                "max-110x110"
            ).url

        # Try to parse the salary_range, otherwise the searchable_salary.
        for salary in (self.salary_range, self.searchable_salary):
            try:
                min_salary, max_salary = extract_salary_range(salary)
            except TypeError:
                pass
            else:
                markup["baseSalary"] = {
                    "@type": "MonetaryAmount",
                    "currency": "GBP",
                    "value": {"@type": "QuantitativeValue", "unitText": "YEAR"},
                }
                if min_salary:
                    markup["baseSalary"]["value"]["minValue"] = min_salary
                if max_salary:
                    markup["baseSalary"]["value"]["maxValue"] = max_salary
                break

        if self.location_lat and self.location_lon:
            markup["jobLocation"]["latitude"] = str(self.location_lat)
            markup["jobLocation"]["longitude"] = str(self.location_lon)

        return mark_safe(json.dumps(markup))


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


@register_snippet
class AwardsSnippet(models.Model):
    heading = models.CharField(max_length=255)
    awards = StreamField([("award", AwardBlock())], use_json_field=True)

    panels = [
        FieldPanel("heading"),
        FieldPanel("awards"),
    ]

    def __str__(self):
        return self.heading


@register_snippet
class JobPlatformsMediaSnippet(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    cta = models.CharField(max_length=255, verbose_name="Call to action text")
    job_platforms = StreamField([("platform", JobPlatformBlock())], use_json_field=True)
    media_embed = StreamField(MediaBlock(), max_num=1, use_json_field=True)

    def __str__(self):
        return self.title


class RecruitmentHomePage(RoutablePageMixin, BasePage):
    template = "patterns/pages/home/home_page--jobs.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    job_board = models.CharField(max_length=20, blank=True, unique=True)
    hero_title = models.CharField(
        max_length=255, help_text="e.g. Finding a job in Buckinghamshire"
    )
    hero_subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. Over 100 job opportunities available daily.",
    )
    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    search_box_placeholder = models.CharField(
        max_length=255,
        help_text="eg. Search jobs, e.g. “Teacher in Aylesbury”",
    )
    hero_link_text = models.CharField(max_length=255, help_text="e.g. Browse jobs")
    awards = models.ForeignKey(
        "recruitment.AwardsSnippet",
        verbose_name="Awards snippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    media = models.ForeignKey(
        "recruitment.JobPlatformsMediaSnippet",
        verbose_name="Job platforms media snippet",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
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
        use_json_field=True,
    )
    related_recruitment_index_page = models.ForeignKey(
        "recruitment.RecruitmentIndexPage",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        help_text="The page whose “top 6” child pages will be displayed as cards on the current page",
    )
    recruitment_index_link_text = models.CharField(
        verbose_name="Related recruitment index page link text",
        max_length=255,
        blank=True,
        help_text="e.g. If blank, a default of 'Visit our guide page' will be used",
    )

    search_fields = BasePage.search_fields + [index.SearchField("hero_title")]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_image"),
                FieldPanel("search_box_placeholder"),
                FieldPanel("hero_link_text"),
            ],
            "Hero",
        ),
        FieldPanel("body"),
        FieldPanel("media"),
        FieldPanel("awards"),
        FieldPanel("related_recruitment_index_page"),
        FieldPanel("recruitment_index_link_text"),
    ]
    settings_panels = BasePage.settings_panels + [
        FieldPanel(
            "job_board",
            widget=forms.Select(
                choices=[(s, s) for s in JOB_BOARD_CHOICES],
            ),
        ),
    ]

    def get_related_recruitment_index_page_subpages(self):
        """
        Return the first 6 subpages of the specified related_recruitment_index_page

        NOTE: in the template, the first 3 subpages are rendered with images,
        while the images are not rendered for the last three.
        """
        if self.related_recruitment_index_page:
            return self.related_recruitment_index_page.child_pages[:6]
        return Page.objects.none()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["benefits_list"] = self.get_related_recruitment_index_page_subpages()
        context["job_categories"] = JobCategory.get_categories_summary(homepage=self)

        return context

    def get_sitemap_urls(self, request=None):
        sitemap = super().get_sitemap_urls(request)

        today = date.today()
        jobs = TalentLinkJob.objects.filter(
            posting_start_date__lte=today, posting_end_date__gte=today, homepage=self
        )

        jobs_sitemap = []
        for job in jobs:
            jobs_sitemap.append(
                {
                    "location": self.full_url
                    + self.reverse_subpage(
                        "job_detail",
                        args=(job.talentlink_id,),
                    ),
                    "lastmod": job.last_modified,
                }
            )
            if job.show_apply_button:
                jobs_sitemap.append(
                    {"location": job.application_url, "lastmod": job.last_modified}
                )

        return sitemap + jobs_sitemap

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
        try:
            job_id = request.GET.get("jobId")
            if job_id and "-" in job_id:
                talentlink_id = job_id.split("-")[1]
                page = TalentLinkJob.objects.get(talentlink_id=talentlink_id)
            else:
                raise Http404("Missing job details")
        except ValueError:
            # This is raised if casting the job_id to an int fails in the query
            raise Http404("Could not determine job details from URL")
        except TalentLinkJob.DoesNotExist:
            # We don't have a job to display as a page title. The JavaScript application
            # component independently fetches jobs from the API, so we display a generic
            # title then defer to that to try to render a non-imported application form.
            show_sidebar = False
            page = {"title": "Application form"}
        else:
            show_sidebar = True
        return render(
            request,
            "patterns/pages/jobs/apply.html",
            {
                "page": page,
                "show_apply_button": False,
                "show_sidebar": show_sidebar,
                "apply_config_key": getattr(
                    settings, "TALENTLINK_APPLY_CONFIG_KEY_" + self.job_board.upper()
                ),  # Will throw AttributeError if not defined
            },
        )


class RecruitmentIndexPage(BasePage):
    template = "patterns/pages/standardpages/index_page--jobs.html"
    parent_page_types = ["recruitment.recruitmenthomepage"]

    hero_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    hero_subtitle = models.CharField(
        max_length=255,
        blank=True,
    )
    body = StreamField(StoryBlock(required=False), blank=True, use_json_field=True)

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_image"),
            ],
            "Hero",
        ),
        FieldPanel("body"),
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
    homepage = models.ForeignKey(
        "RecruitmentHomePage", on_delete=models.CASCADE, blank=True, null=True
    )
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, unique=True, editable=False)

    @cached_property
    def prettified_search(self):
        search_params = json.loads(self.search)
        # Rename the key, 'query' to something nicer
        if "query" in search_params:
            search_params["search term"] = search_params.pop("query")
        # Replace category slugs with category titles
        if "category" in search_params:
            search_params["category"] = list(
                JobCategory.objects.filter(
                    slug__in=search_params["category"]
                ).values_list("title", flat=True)
            )
        return search_params

    @cached_property
    def site_url(self):
        return self.homepage.url.rstrip("/")

    @property
    def confirmation_url(self):
        return reverse("confirm_job_alert", args=[self.token])

    @property
    def unsubscribe_url(self):
        return reverse("unsubscribe_job_alert", args=[self.token])

    def full_clean(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        if not self.homepage:
            self.homepage = RecruitmentHomePage.objects.live().first()

        super().full_clean(*args, **kwargs)

    def get_email_context(self):
        context = {}
        context["search_criteria"] = self.prettified_search
        context["confirmation_url"] = self.site_url + self.confirmation_url
        context["unsubscribe_url"] = self.site_url + self.unsubscribe_url
        return context

    def send_confirmation_email(self):
        template_name = "patterns/email/confirm_job_alert.txt"
        context = self.get_email_context()
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
