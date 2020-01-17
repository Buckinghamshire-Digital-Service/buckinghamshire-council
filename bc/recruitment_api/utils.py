from dateutil.parser import parse


def date_parser(value):
    return parse(value, dayfirst=True)


def string_parser(value):
    return value.strip()


def yesno_parser(value):
    return value.lower() == "yes"


POSTING_TARGET_STATUS_PUBLISHED = "Published"

# source field to (target_field, parser) mapping
JOB_CONFIGURABLE_FIELDS_MAPPING = {"Closing Date": ("closing_date", date_parser)}

JOB_CUSTOM_LOVS_MAPPING = {
    "Job Group": ("category", string_parser),
    "Location": ("location", string_parser),
    "Salary Range - FTE": ("salary_range", string_parser),
    "Searchable Location": ("searchable_location", string_parser),
    "Searchable Salary": ("searchable_salary", string_parser),
    "Show Apply Button": ("show_apply_button", yesno_parser),
    "Working Hours Selection": ("working_hours", string_parser),
}


def update_job_from_ad(job, ad):
    job.job_number = ad["jobNumber"]
    job.title = ad["jobTitle"]
    job.is_published = ad["postingTargetStatus"] == POSTING_TARGET_STATUS_PUBLISHED
    job.posting_start_date = ad["postingStartDate"]
    job.posting_end_date = ad["postingEndDate"]

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
    for custom_field in ad["customFields"]["customField"]:
        if custom_field["value"]:
            description.append(f"<h2>{custom_field['label'].strip()}</h2>")
            description.append(custom_field["value"].strip())
    job.description = "\n".join(description)

    for custom_lov in ad["customLovs"]["customLov"]:
        try:
            target_field, parser = JOB_CUSTOM_LOVS_MAPPING[custom_lov["label"]]
        except KeyError:
            pass
        else:
            setattr(
                job,
                target_field,
                parser(custom_lov["criteria"]["criterion"][0]["label"]),
            )
    job.save()
    return job
