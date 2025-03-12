# Hosting

The VM comes preinstalled with Fabric, Heroku CLI and AWS CLI.

## Deployed Instances

| Instance     | Branch    | URL                                                           | Heroku                         |
| ------------ | --------- | ------------------------------------------------------------- | ------------------------------ |
| Production   | `master`  | https://www.buckinghamshire.gov.uk                            | `buckinghamshire-production`   |
| Staging      | `staging` | https://buckinghamshire-staging.staging.torchbox.com          | `buckinghamshire-staging`      |
| Content Prep | `master`  | https://buckinghamshire-content-prep.production.torchbox.com/ | `buckinghamshire-content-prep` |

Each instance has several subdomain URLs for:

- Recruitment site
- Internal recruitment site
- Family Information Service
- Care Advice Bucks

See the `ALLOWED_HOSTS` environment variable and the Wagtail Sites settings on each instance for up to date details.

## Log in to Heroku

Please log in to Heroku before executing any commands for servers hosted there
using the `Heroku login -i` command. You have to do it both in the VM and your
host machine if you want to be able to use it in both places.

## Connect to the shell

To open the shell of the servers.

```bash
fab staging-shell
fab production-shell
fab content-prep-shell
```

## Scheduled tasks

When you set up a server you should make sure the following scheduled tasks are set.

- `django-admin publish_scheduled_pages` - every 10 minutes or more often. This is necessary to make publishing scheduled pages work.
- `django-admin clearsessions` - once a day (not necessary, but useful).
- `django-admin update_index` - once a day (not necessary, but useful to make sure the search index stays intact).
- `django-admin searchpromotions_garbage_collect` - once a day (by default 30 days of search hits will be retained, but it can be configured using the `WAGTAILSEARCH_HITS_MAX_AGE` environment variable).
