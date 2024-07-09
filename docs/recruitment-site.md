# Recruitment Site

This is hosted at https://jobs.buckinghamshire.gov.uk/. It is a Django/Wagtail app sitting within the main project, with a set of page types for this site only, including its own home page type.

# Internal Recruitment Site

There is also a recruitment site for internal jobs. This is hosted on TBC. It is a clone of the main recruitment site with different jobs and job alert associated.

Each recruitment site will display different job listing. Many jobs may be posted to both sites. The jobs on each site will have a different `talentlink_id` though they will share the same `job_number`.

Note that categories and subcategories are shared across the recruitment sites.

## Local development

Either grab a database dump from production or staging, or:

1. At root, add a Job home page
1. Edit sites (/admin/sites/), and add a new site for job homepage, selecting the newly created job homepage as home page
1. Update sites settings:
   1. Update sites settings to use the local domain for job homepage
   1. Update your /etc/hosts with the new job domain if needed. Eg. mine is 127.0.0.1 jobs.bc.local bc.local
1. In VM, run `dj import_jobs` (see below about credentials). You should see something like "Fetching page 1... 140 new jobs created." (If you get `JobCategory.DoesNotExist` errors, run the import command with `dj import_jobs --import_categories`. This will import the missing categories).
1. Jobs are imported as TalentLinkJob models, and not page models. So you won't see the pages. To view a job page, you will need to append `/job_detail/<talentlink_id>/`. Eg. http://jobs.bc.local:8000/job_detail/123/
1. You can view imported jobs in the Wagtail admin at e.g. http://jobs.bc.local:8000/admin/recruitment/talentlinkjob/

## Credentials

The following environment variables must be set to authenticate with the API (or configured in local settings, for dev enviromnents):

- `TALENTLINK_API_KEY`
- `TALENTLINK_API_PASSWORD`
- `TALENTLINK_API_USERNAME_EXTERNAL`
- `TALENTLINK_API_USERNAME_INTERNAL`
- And potentially `TALENTLINK_API_USERNAME_{uppercase job board name}` for any new boards
- `TALENTLINK_APPLY_CONFIG_KEY_EXTERNAL`
- `TALENTLINK_APPLY_CONFIG_KEY_INTERNAL`
- And potentially `TALENTLINK_APPLY_CONFIG_KEY_{uppercase job board name}` for any new boards
- `TALENTLINK_API_WSDL`, this is configurable, but not secret, and should be set to "https://api3.lumesse-talenthub.com/CareerPortal/SOAP/FoAdvert?WSDL"

## SOAP

Jobs are fetched from the Lumesse TalentLink SOAP API. We use [Zeep](https://python-zeep.readthedocs.io/en/master/client.html) as an API client.

API documentation is at https://developer.lumesse-talenthub.com/docs.html. From there we use the "Fo Advert" bundle.

You can use zeep to inspect the (undocumented) WSDL file for that API:

```python
python -mzeep https://api3.lumesse-talenthub.com/CareerPortal/SOAP/FoAdvert?WSDL
```

This is done in code too, at the point where the internal `zeep.Client` is configured. It populates 'service' methods on the client, corresponding to the services documented at https://developer.lumesse-talenthub.com/docs/read/career_portal/FoAdvert.html.

## Zeep

### Authentication with Lumesse TalentLink

The Lumesse TalentLink API uses both WS-Security (the request body contains a username and password in the Header element) and requires an API key to be supplied as a URL query parameter. We have modified the Zeep Transport class to add this API key to all URLs.

### Use with Django cache

Zeep caches WSDL schemata internally. We use a custom `ZeepDjangoBackendCache` to fit with the infrastructure Django already provides. See [Infrastructure](infrastructure.md) for details of the Django backend.

## Lumesse TalentLink API

Every service documented at https://developer.lumesse-talenthub.com/docs/read/career_portal/FoAdvert.html has a corresponding service method on the client, e.g. there's a service in the documentation called 'getAdvertisements', corresponding to the WSLD service of the same name:

```wsld
getAdvertisements(
    firstResult: xsd:int,
    maxResults: xsd:int,
    searchCriteriaDto: ns0:searchCriteriaDto,
    sortingDetailsDto: ns0:sortingDetailsDto,
    langCode: ns0:langCode,
    showJobLocation: xsd:boolean,
    displayFullContent: xsd:boolean) -> advertisementResult: ns0:advertisementResultDto
```

You can call this in Python code with:

```python
>>> from bc.recruitment_api.client import get_client
>>> client = get_client()
>>> resp = client.service.getAdvertisements(1, 10)
>>> resp['totalResults']
136
>>> len(resp['advertisements']['advertisement'])
10
>>> dir(resp['advertisements']['advertisement'][0])
['applicationUrl', 'assignedImages', 'categoryLists', 'comment', 'compensationMaxValue', 'compensationMinValue', 'configurableFields', 'contractCompensationPeriod', 'contractDuration', 'customFields', 'customLovs', 'descriptionUrl', 'dueDate', 'duration', 'expectedEndDate', 'expectedStartDate', 'externalJobNumber', 'generalApplication', 'id', 'indeedConfiguration', 'jobLocations', 'jobNumber', 'jobTitle', 'jobUpdateDate', 'keyword', 'language', 'location', 'operationals', 'organizations', 'postingEndDate', 'postingStartDate', 'postingTargetStatus', 'postingUserEmail', 'recruiters', 'recruitingCompany', 'requisitionInternalJobNumber', 'showCompensation', 'showRecruiter', 'siteLanguage', 'sponsoredJobContext', 'standardLovs', 'standardRate', 'status', 'strapline']
>>> resp['advertisements']['advertisement'][0]['jobTitle']
'2 x Support Workers - Autism - Spring Valley Day Centre / Spectrum Unit'
```

## Saba

Saba is the system used for managing jobs and applications.

Jobs are identified by a unique job number, eg. BUC0003 which corresponds to `TalentLinkJob.job_number` on the Wagtail site.

On Saba, jobs can have multiple advertisements. Advertisements can be posted to multiple targets. Each posting target (ie. job board) has its own TalentLink API credentials. We are currently only importing job advertisements posted to 'External site' and 'Internal site' on Saba.

Each job advertisement posting to a job board will have a start date, end date, and status. It will only appear on the TalentLink API feed for the job board if its status is 'Published'.

The posting will also have a unique ad id which corresponds to `TalentLinkJob.talentlink_id`. This is different for each job board, even if it is from the same job advertisement.

## Importing jobs

The management command `import_jobs` will fetch results from the API.

If the `--import_categories` option is specified when running the `import_jobs` command, new categories will be imported. Otherwise, jobs with categories that do not match existing `JobSubcategory` instances will be skipped in the import.

`JobSubcategory` objects are unique by title, but looked up case-insensitively by the importer. This is due to similar entries like "Schools secondary" and "Schools Secondary" in the source data.

Note that the imported `Job Group` attribute from the API is mapped to the `JobSubcategory` model in Django, but that users can filter by either category or subcategory. The relationship between categories and their subcategories can be edited in the Wagtail admin.

### Job Boards (ie. External and Internal job sites)

Jobs on TalentLink can be posted to multiple job boards (eg. External or Internal). The job board is set on the recruitment homepage (go to the Settings tab).

Each TalentLinkJob instance belongs to only one recruitment site.

The import script loops through the instances of recruitment homepage on the system and import jobs for the job board defined on the instance.

If a corresponding API_USERNANE for the job board (eg. `settings.TALENTLINK_API_USERNAME_EXTERNAL`) is not defined on settings, import will be skipped for the recruitment site.

### Imported fields

This is a non-exhaustive reference of the fields we map from the API return. It serves to highlight some of the noteworthy aspects:

#### Description

This is a concatenation of multiple `custom_field` fields, whose format is a 'label' and a 'value'. We turn the label into a `<h3>` element, and the value into a paragraph, but we also strip out most HTML formatting, according to a whitelist of tags and their attributes in `bc.recruitment_api.constants`.

#### Short description

This is either the text of the first `<p>` element in the first custom_field value from above, or the entire first custom_field value, if it is formatted as plain text.

#### Logo

Logo images are pulled from their remote location and imported to Wagtail's image library. If an image doesn't pass Wagtail's validation, it's rejected and the field left blank. This means that some images allowed by TalentLink may not be imported - e.g. if they exceed the size allowed by the `MAX_IMAGE_PIXELS` setting.

## Job Alerts

### Management command

```python
dj send_job_alerts
```

This searches for new matches for all confirmed job alert subscriptions.

A new match is any job whose created date is since the start of the last successful run, and since the alert was created.

The way the command is written intends it to be called daily, but other durations shouldn't matter, so long as the duration is longer than the time taken for the command to run. It specifically ignores jobs imported during the running of the alert command, leaving them for the next alert cycle.

Job alerts are site specific.

## Application forms

This function is provided by the RAC, Responsive Application Component, a front-end application developed and supplied as-is by Saba Talentlink.

This was originally developed by them and styled to match the previous county council's recruitment site, but is now styled by us.

The vendor static files are in `/bc/static_src/vendor/talentlink/`, (though only the JS is still in use), and the HTML in `bc/project_styleguide/templates/patterns/pages/jobs/apply.html`. We have kept the layout of the HTML file fairly close to the originally-supplied file, with commented-out header tags etc., to make it easier to understand the diff in future if an updated file is supplied by Saba.
