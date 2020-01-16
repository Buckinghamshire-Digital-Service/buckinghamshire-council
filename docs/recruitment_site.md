# Recruitment Site

This is hosted at https://jobs.buckinghamshire.gov.uk/. It is a Django/Wagtail app sitting within the main project, with a set of page types for this site only, including its own home page type.

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

Zeep caches WSDL schemata internally. We use a custom `ZeepDjangoBackendCache` to fit with the infrastructure Django already provides.

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

## Importing jobs

The management command `import_jobs` will fetch results from the API.
