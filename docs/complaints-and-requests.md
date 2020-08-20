# Complaints and Request Forms

This document covers those forms which integrate with the Aptean Respond case management platform.

Some other forms within the project are implemented using Wagtail's Forms contrib module, and are not covered here.

## Background

The company Aptean produces a platform called Respond, which tracks customer enquiry 'cases'. It is a REST API using XML. Documentation is only available in PDFs, which are generally available from the client as email attachments.

Note that the documentation is terse, has differing variable naming standards (`schema-name` vs `schemaName`), differing parameters between example request payloads (some specify a per-field `data-type` attribute, some not), syntax errors in the example XML schemata (in addition to any errors got by copying and pasting from the PDF document, which adds headers and footers and mangles line breaks), and example XML request payloads that do not validate against those schemata.

The web services available in the API are configured by council staff in a desktop program called "Configuration Manager". We use the following endpoints:

- _Web Service Meta Data Service_, to list the web services configured in configuration manager
- _Create Case Service_, to POST a user's form submission
- _Get Fields Service_, to get the properties of a field (mainly 'required')
- _Get Categories Service_, to get the valid choices for a 'category' field (i.e. any represented by a select input)

We have asked the client to configure the _Get Fields Service_ and _Get Categories Service_ to contain data for all fields, which we cache in our application client and use to build the form information.

Note that the _Get Fields Service_ does not allow the council staff to specify the order of fields in a case. That is defined in our application. The fields they can add are only those defined by Aptean. Custom fields at the API level are, generally, not possible.

Any custom properties, such as the labels, help_text, removing of `choices` options, and overriding of `required` properties is done in Python code. In several cases we add custom fields to the form which are processed and appended to the description before submission.

The form UX in the designs is much more complicated than this allows, so further features are added in our application.

## Credentials

The following environment variables must be set to authenticate with the API (or configured in local settings, for dev enviromnents):

- `RESPOND_API_USERNAME`
- `RESPOND_API_PASSWORD`
- `RESPOND_API_DATABASE` — "Prod" or "Test"
- `RESPOND_API_BASE_URL` — set this to "https://groupc.respond.apteancloud.com/Buckinghamshire/ws/"

We also define the names of the CreateCase-type services that we wish to 'register'.

- `RESPOND_COMPLAINTS_WEBSERVICE` e.g. "TestCreateComplaints"
- `RESPOND_FOI_WEBSERVICE`
- `RESPOND_SAR_WEBSERVICE`
- `RESPOND_COMMENTS_WEBSERVICE`
- `RESPOND_COMPLIMENTS_WEBSERVICE`
- `RESPOND_DISCLOSURES_WEBSERVICE`

## API Client

The API client is loaded when first needed by `bc.cases.backends.respond.client.get_client()` and remains in memory.

There is a page type `bc.cases.models.ApteanRespondFormPage`, which has a field `form`. This determines what form should load for the page.

The form classes all inherit from `bc.cases.backends.respond.forms.BaseCaseForm`, which handles producing XML for the API.

### XML

Typically within the application, API XML responses are parsed with Beautiful Soup, but XML request payloads are assembled with `lxml.etree`. These have different internal APIs, so watch out for that.

The `bc.cases.backends.respond.forms.BaseCaseForm` class has a method `self.get_xml(cleaned_data)` to return the payload for an API request.

### Append-to-description fields

All form fields to be submitted to the API must either be mapped in the form's `.field_schema_name_mapping` attribute. If no suitable schema name exists in the API web service definition, the field name must be included in the form's `.append_to_description_fields` property. The label and cleaned value of these fields will be appended to the description field before form submission.
