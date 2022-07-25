from urllib.parse import urlsplit

from django.core.files.base import ContentFile
from django.utils.html import strip_tags

from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup
from dateutil.parser import parse
from zeep.helpers import serialize_object

from bc.documents.models import CustomDocument
from bc.recruitment_api.client import get_client

from ..recruitment.models import JobSubcategory, TalentLinkJob
from . import constants


def date_parser(value):
    return parse(value, dayfirst=True)


def string_parser(value):
    # Remove multiple spaces as well as trailing and end spaces.
    return " ".join(value.split())


def yesno_parser(value):
    return value.lower() == "yes"


def job_subcategory_parser(value):
    """Get existing JobSubcategory

    If subcategory does not exist, we don't want to import this job.
    This will throw a `JobSubcategory.DoesNotExist` error
    which will be handled by the calling import_jobs command.
    """
    clean_value = string_parser(value)
    return JobSubcategory.objects.get(title__iexact=clean_value)


def job_subcategory_insert_parser(value):
    """Get or create existing JobSubcategory"""
    clean_value = string_parser(value)
    subcategory_object, created = JobSubcategory.objects.get_or_create(
        title__iexact=clean_value, defaults={"title": clean_value}
    )
    return subcategory_object


POSTING_TARGET_STATUS_PUBLISHED = "Published"

# source field to (target_field, parser) mapping
JOB_CONFIGURABLE_FIELDS_MAPPING = {
    "Contact Information": ("contact_email", string_parser),
    "Closing Date": ("closing_date", date_parser),
    "Interview Information": ("interview_date", date_parser),
}

JOB_LOVS_MAPPING = {
    "Job Group": ("subcategory", job_subcategory_parser),
    "Salary Range": ("salary_range", string_parser),
    "Searchable Salary": ("searchable_salary", string_parser),
    "Show Apply Button": ("show_apply_button", yesno_parser),
    "Working Hours Selection": ("working_hours", string_parser),
    "Contract Type": ("contract_type", string_parser),
    # Label of DBS check according to example job. See also:
    # https://trello.com/c/dm4XuwPh/66-the-recruitment-team-have-requested-a-change-to-the-front-end-presentation-within-the-jobsbuckinghamshiregovuk-page-to-show-whet#comment-60e850464897b75ea4e82323
    "Does the role require a DBS check?": ("dbs_check", string_parser),
}


def update_job_from_ad(job, ad, homepage, defaults=None, import_categories=False):
    defaults = defaults or {}

    cleaner = Cleaner(
        tags=constants.BLEACH_ALLOWED_TAGS,
        attributes=constants.BLEACH_ALLOWED_ATTRIBUTES,
        strip=True,
    )

    job.homepage = homepage
    job.job_number = ad["jobNumber"]
    job.title = ad["jobTitle"].strip()
    job.is_published = ad["postingTargetStatus"] == POSTING_TARGET_STATUS_PUBLISHED
    job.posting_start_date = ad["postingStartDate"]
    job.posting_end_date = ad["postingEndDate"]
    job.expected_start_date = ad["expectedStartDate"]
    job.application_url_query = urlsplit(ad["applicationUrl"]).query

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

    # CustomLovs and StandardLovs
    for lov in ad["customLovs"]["customLov"] + ad["standardLovs"]["standardLov"]:
        try:
            target_field, parser = JOB_LOVS_MAPPING[lov["label"]]
        except KeyError:
            pass
        else:
            # Use insert subcategory parser if command specifies `--import_categories`
            if (parser is job_subcategory_parser) and import_categories:
                parser = job_subcategory_insert_parser

            setattr(job, target_field, parser(lov["criteria"]["criterion"][0]["label"]))
    for k, v in defaults.items():
        setattr(job, k, v)

    # Get location data
    if ad["jobLocations"]:
        # Unit tests provide dicts, the Zeep library provides Zeep objects. We convert
        # Zeep instance to native Python OrderedDict, so we can use obj.get() for
        # everything. NB this also serializes Python dicts to OrderedDicts.
        location = serialize_object(ad["jobLocations"]["jobLocation"][0])
        for ad_attr, job_attr in [
            ("location_name", "location_name"),
            ("streetNumber", "location_street_number"),
            ("street", "location_street"),
            ("city", "location_city"),
            ("region", "location_region"),
            ("country", "location_country"),
            ("zipCode", "location_postcode"),
            ("latitude", "location_lat"),
            ("longitude", "location_lon"),
        ]:
            value = location.get(ad_attr)
            if value:
                setattr(job, job_attr, value)

    job.organisation = " — ".join(
        [
            organisation["value"]
            for organisation in sorted(
                ad["organizations"]["organization"],
                key=lambda organisation: organisation["level"],
            )
        ]
    )

    job.save()
    return job


def delete_jobs(imported_before, homepage):
    """Delete outdated TalentLinkJob objects

    Args:
        imported_before (datetime): Cutoff datetime for jobs `last_imported` values.

    Returns:
        (int) The number of jobs deleted.

    """

    outdated_jobs = TalentLinkJob.objects.filter(homepage=homepage).filter(
        last_imported__lt=imported_before
    )
    count = outdated_jobs.count()
    outdated_jobs.delete()

    return count


def import_attachments_for_job(job, client=None):
    doc_imported = 0
    if not client:
        client = get_client(job_board=job.homepage.job_board)

    # This will return list of attachments with
    #   'content', 'description', 'fileName', 'id', 'mimeType'
    attachments_response = client.service.getAttachments(job.talentlink_id)
    for attachment in attachments_response:
        if attachment["id"] and attachment["fileName"]:
            doc, created = CustomDocument.objects.get_or_create(
                talentlink_attachment_id=attachment["id"]
            )
            if created:
                doc.title = (
                    attachment["description"] or attachment["fileName"].split(".")[0]
                )
                doc.file = ContentFile(
                    attachment["content"],
                    name=attachment["fileName"],
                )
                doc.save()
                doc_imported += 1

            job.attachments.add(doc)
            job.save()

    return doc_imported
