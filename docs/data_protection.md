# Buckinghamshire Council — Data Protection

See also: [Cookies](cookies.md)

This page gives an overview of potentially-sensitive data stored or processed by the Buckinghamshire Council project.

### User accounts

Buckinghamshire Council Wagtail user accounts store a user's name and email address.

### Other

#### Wagtail Forms submissions

These can store any type of data, as they are configured by the editors at Buckinghamshire Council.

Responsibility for ensuring GDPR compliance in the normal storage and processing of this data rests with the client, Buckinghamshire Council.

When duplicating the database for development purposes, developers are responsible for deleting these records from duplicates. See _Data locations_ below.

#### Aptean forms submissions

These submissions, part of the `bc.cases` app, are processed by Django view functions, but data is not stored in our application. Form submissions are posted via HTTPS to the Aptean Forms API. We also process responses to those submissions, which may contain PII if the response is an error message.

### Other non-issues

These are common sources of personal data which are _not_ handled by the Buckinghamshire Council Django application.

#### Newsletter subscription requests

These requests are handled by sending the users to a third party, where PII is handled. The Django application does not handle any such data directly or indirectly.

#### Job applications

These requests are handled by a third-party provider. The code which processes data is JavaScript hosted on our site, but provided by the third-party, and posting to an external API. Our servers do not process or store any personally-identifying data.

## Data locations

Data is stored in the database, in the models:

- `bc.recruitment.models.JobAlertSubscription`
- `bc.users.models.User`
- `wagtail.contrib.forms.models.FormSubmission`

All backups, automated or otherwise, include this data.

All exports include this data. The first steps when downloading a copy of the production database, or cloning it to staging, should be to delete all records in the above tables.

Personally-identifying data may also appear in error reports, at sentry.io. We have configured the Sentry project to anonymise known sensitive fields, including some bespoke fields for this project, such as for Aptean forms submissions.

## Responding to GDPR requests

If a request is received to purge or report the stored data for a given user, what steps are needed?

- For user account data, delete the user from the Wagtail admin https://www.buckinghamshire.gov.uk/admin/users/
- For form submissions, ask the client to handle requests as the first option. Failing that, search the submissions and delete if necessary using the Django shell.
- For JobAlertsSubscriptions, find and delete from https://www.buckinghamshire.gov.uk/admin/recruitment/jobalertsubscription/

Note: this will not purge such data from backups.
