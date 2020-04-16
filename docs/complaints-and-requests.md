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

Constructing the client, and the forms.

1. The API client is loaded when first needed by `bc.cases.backends.respond.client.get_client()` and remains in memory.
1. It parses the web services defined in Aptean Respond, registers CreateCase-type services defined in `bc.cases.backends.respond.constants.CREATE_CASE_SERVICES`, and uses the Django low-level cache (with no timeouts) to store _Get Fields Service_ and _Get Categories Service_ responses.
1. It then uses `bc.cases.backends.respond.forms.CaseFormBuilder`, a class inspired by Wagtail's FormBuilder, to assemble a form, taking the registered create case service's XML definition as its input, and replaces the XML in `client.services[CREATE_CASE_TYPE]` with those forms instead.

There is a page type `bc.cases.models.ApteanRespondFormPage`, which has a field `web_service_definition`. This again mimics `FormPage` from Wagtail's forms module, and uses the form stored at `client.services[CREATE_CASE_TYPE][self.web_service_definition]`.

### XML

Typically within the application, API XML responses are parsed with Beautiful Soup, but XML request payloads are assembled with `lxml.etree`. These have different internal APIs, so watch out for that.

The `bc.cases.backends.respond.forms.BaseCaseForm` class has a method `self.get_xml(cleaned_data)` to return the payload for an API request.

## Form customisation

We can override the field properties of the generated forms. See `bc.cases.backends.respond.constants.CREATE_CASE_SERVICES`.

### Append-to-description fields

All fields in the generated FormBuilder forms have names matching their XML SchemaName. One particular field type, generated only in our app, uses the schema name format `"append to description.some_unique_field_name"`. These fields do not exist in the API, and their label and cleaned value are appended to the description field before form submission.
