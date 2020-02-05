from django.utils.html import strip_tags

from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup
from dateutil.parser import parse

from ..recruitment.models import JobCategory
from . import constants


def date_parser(value):
    return parse(value, dayfirst=True)


def string_parser(value):
    return value.strip()


def yesno_parser(value):
    return value.lower() == "yes"


def job_category_parser(value):
    """Get existing JobCategory

    If category does not exist, we don't want to import this job.
    This will throw a `JobCategory.DoesNotExist` error
    which will be handled by the calling import_jobs command.
    """
    clean_value = string_parser(value)
    return JobCategory.objects.get(title=clean_value)


def job_category_insert_parser(value):
    """Get or create existing JobCategory"""
    clean_value = string_parser(value)
    category_object, created = JobCategory.objects.get_or_create(title=clean_value)
    return category_object


POSTING_TARGET_STATUS_PUBLISHED = "Published"

# source field to (target_field, parser) mapping
JOB_CONFIGURABLE_FIELDS_MAPPING = {"Closing Date": ("closing_date", date_parser)}

JOB_CUSTOM_LOVS_MAPPING = {
    "Job Group": ("category", job_category_parser),
    "Location": ("location", string_parser),
    "Salary Range - FTE": ("salary_range", string_parser),
    "Searchable Location": ("searchable_location", string_parser),
    "Searchable Salary": ("searchable_salary", string_parser),
    "Show Apply Button": ("show_apply_button", yesno_parser),
    "Working Hours Selection": ("working_hours", string_parser),
}


def update_job_from_ad(job, ad, defaults=None, import_categories=False):
    defaults = defaults or {}

    cleaner = Cleaner(
        tags=constants.BLEACH_ALLOWED_TAGS,
        attributes=constants.BLEACH_ALLOWED_ATTRIBUTES,
        strip=True,
    )

    job.job_number = ad["jobNumber"]
    job.title = ad["jobTitle"]
    job.is_published = ad["postingTargetStatus"] == POSTING_TARGET_STATUS_PUBLISHED
    job.posting_start_date = ad["postingStartDate"]
    job.posting_end_date = ad["postingEndDate"]
    job.expected_start_date = ad["expectedStartDate"]

    for configurable_field in ad["configurableFields"]["configurableField"]:
        try:
            target_field, parser = JOB_CONFIGURABLE_FIELDS_MAPPING[
                configurable_field["label"]
            ]
        except KeyError:
            pass
        else:
            setattr(
                job,
                target_field,
                parser(configurable_field["criteria"]["criterion"][0]["value"]),
            )

    # The description is conveyed in 'custom' fields, where the label acts as a subheading
    description = []
    custom_fields = sorted(ad["customFields"]["customField"], key=lambda x: x["order"])
    for i, custom_field in enumerate(custom_fields):
        if custom_field["value"]:
            description.append(f"<h3>{custom_field['label'].strip()}</h3>")
            description.append(cleaner.clean(custom_field["value"]))
            if i == 0:
                soup = BeautifulSoup(custom_field["value"], "html.parser")
                if soup.find("p"):
                    text = soup.find("p").text
                else:
                    # The value is plaintext, or at least contains no p tags
                    text = strip_tags(custom_field["value"])

                job.short_description = cleaner.clean(" ".join(text.split()))

    job.description = "\n".join(description)

    for custom_lov in ad["customLovs"]["customLov"]:
        try:
            target_field, parser = JOB_CUSTOM_LOVS_MAPPING[custom_lov["label"]]
        except KeyError:
            pass
        else:
            # Use insert category parser if command specifies `--import_categories`
            if (parser is job_category_parser) and import_categories:
                parser = job_category_insert_parser

            setattr(
                job,
                target_field,
                parser(custom_lov["criteria"]["criterion"][0]["label"]),
            )
    for k, v in defaults.items():
        setattr(job, k, v)
    job.save()
    return job
