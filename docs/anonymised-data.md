# Buckinghamshire Council Anonymising Data

## General principles:

- pull data from staging rather than production servers, if this is good enough for your needs
- if it is necessary to pull data from production, e.g. for troubleshooting, consider whether anonymising personal data is possible and compatible with your needs
- if it is necessary to pull non-anonymised data from production, consider destroying this copy of the data as soon as you no longer need it

In more sensitive cases, consider a data protection policy to prevent access to production data except for authorised users.

## Anonymise

`django-birdbath` provides a management command (`run_birdbath`) that will anonymise the database.

As and when models/fields are added that may be populated with sensitive data (such as email addresses) a processor should be added to ensure that the data can be anonymised or deleted when it is copied from the production environment.

For full documentation see https://git.torchbox.com/internal/django-birdbath/-/blob/master/README.md.

### Data processors

The data processors can be found in [base.py](../bc/settings/base.py)

```python
BIRDBATH_PROCESSORS = [
    "birdbath.processors.users.UserEmailAnonymiser",
    "birdbath.processors.users.UserPasswordAnonymiser",
    "birdbath.processors.contrib.wagtail.FormSubmissionCleaner",
    "birdbath.processors.contrib.wagtail.SearchQueryCleaner",
    "bc.blogs.birdbath.DeleteAllBlogAlertSubscriptionProcessor",
    "bc.recruitment.birdbath.DeleteAllRecruitmentAlertSubscriptionProcessor",
]
```

The `flightpath` tool can be used to copy production data (and media) from the production environment to staging. It will automatically `run_birdbath` immediately following this sync operation. A manual CI action is included that will trigger flightpath to sync the environments.

Intended workflow:

1. production data is synced to staging by flightpath
   - birdbath anonymises staging database
2. anonymised data is pulled from **staging** to development environments

This workfow should mean that un-anonymised data is never present on a developer's machine. If data directly from **production** is required, then `run_birdbath` command should be run immediately after download.
