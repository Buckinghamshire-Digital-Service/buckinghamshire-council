# Data Protection

See also: [Cookies](cookies.md)

This page gives an overview of personally-identifying information (PII) stored or processed by the Buckinghamshire Council project.

### User accounts

Buckinghamshire Council Wagtail user accounts store a user's name and email address.

### Other

#### Wagtail Forms submissions

These can store any type of data, as they are configured by the editors at Buckinghamshire Council.

Responsibility for the definition and use of form fields, and their compliance with the GDPR, rests with the Data Controller, Buckinghamshire Council.

When duplicating the database for development purposes, developers are responsible for deleting these records from duplicates. See _Data locations_ below.

#### Aptean forms submissions

These submissions, part of the `bc.cases` app, are processed by Django view functions, but data is not stored in our application. Form submissions are posted via HTTPS to the Aptean Forms API. We also process responses to those submissions, which may contain PII if the response is an error message. Form field error messages are merely displayed to the user where possible, but may be stored in Sentry if a server error is caused. See _Data locations > Error logs_ below.

### Other personal data handling

These are common sources of personal data which are _not_ handled by the Buckinghamshire Council Django application.

#### Newsletter subscription requests

These requests are handled by sending the users to a third party, where PII is handled. The Django application does not handle any such data directly or indirectly.

#### Job applications

These requests are handled by a third-party provider. The code which processes data is JavaScript hosted on our site, but provided by the third-party, and posting to an external API. Our servers do not process or store any personally-identifying data.

## Data locations

PII is stored in the database, in the models:

- `bc.recruitment.models.JobAlertSubscription`
- `bc.users.models.User`
- `wagtail.contrib.forms.models.FormSubmission` (Wagtail FormPage instances)

Potentially users submit feedback form responses which store personally identifying information in the model `bc.feedback.models.FeedbackComment`, though this is not invited.

All backups, automated or otherwise, include this data.

### Exports

All exports include the above data. The first steps when downloading a copy of the production database, or cloning it to staging, should be to delete all records in the user-submitted tables:

```bash
$ python manage.py shell_plus
>>> JobAlertSubscription.objects.all().delete()
>>> FormSubmission.objects.all().delete()
>>> FeedbackComment.objects.all().delete()
```

When copying the data to staging, you probably want to leave user accounts intact, as users are not members of the public and will still want to access the staging site. If using the data locally, you should anonymise user accounts:

```bash
$ python manage.py shell_plus
>>> for user in User.objects.all():
...     user.first_name = "User"
...     user.last_name = user.id
...     user.email = f"user.{user.id}@example.com"
...     user.username = f"user.{user.id}"
...     user.save()
```

### Error logs

Personally-identifying data may also appear in error reports, at sentry.io. We have configured the Sentry project to anonymise known sensitive fields, including some bespoke fields for this project, such as for Aptean forms submissions.

## Responding to GDPR requests

If a request is received to purge or report the stored data for a given user, what steps are needed?

- For user account data, delete the user from the Wagtail admin https://www.buckinghamshire.gov.uk/admin/users/
- For form submissions, ask the client to handle requests as a first option. Failing that, search the submissions and delete if necessary using the Django shell.
- For JobAlertsSubscriptions, find and delete from https://www.buckinghamshire.gov.uk/admin/recruitment/jobalertsubscription/
- For page feedback data, find either from the report in the Wagtail admin or via the Django shell, then delete using the Django shell.

Note: this will not purge such data from backups.
