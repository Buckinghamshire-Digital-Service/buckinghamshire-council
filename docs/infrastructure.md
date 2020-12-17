Buckinghamshire Council Infrastructure

## Database

Postgres

#### Pulling data

To populate your local database with the content of staging/production:

```bash
fab pull-dev-data
fab pull-staging-data
fab pull-production-data
```

To fetch images and other media:

```bash
fab pull-dev-media
fab pull-staging-media
fab pull-production-media
```

## Cache

### Front end

We use Cloudflare's front-end caching for the production site, according to request response headers.

Cache purging is enabled as per https://docs.wagtail.io/en/stable/reference/contrib/frontendcache.html#cloudflare, using the limited-access API Token option, and a token with `Zone.Cache Purge` permission.

### Back end

We use Redis for back-end caching in Django.

The Django low-level cache API is used by the recruitment API client to replace Zeep's default cache. See [Recruitment Site](recruitment-site.md) for details.

## Search engine

The search backend on staging and production is Elasticsearch, provided by Bonsai. See `heroku addons -a buckinghamshire-staging` (or "production"). To view the admin UI, `heroku addons:open bonsai -a buckinghamshire-staging` (or "production").

The recruitment site uses Postgres for search. See `bc.recruitment.utils.get_job_search_results()`.

### Synonyms

Search synonyms can be edited in the Wagtail admin, where any terms in the `synonyms` field will match any records whose index contains the term in the `canonical_term` field. Changes to the configured synonyms will not take place until the search is reindexed.

### Developing the Elasticsearch search engine configuration

The Vagrant box will default to using Postgres for search, and ignoring some of the extra search features such as synonyms. However, it does have Elasticsearch5 installed. To use this, set the search backend in local settings to `bc.search.elasticsearch5` and the URL to "http://localhost:9200".

Alternatively, use a free Bonsai sandbox Elasticsearch instance, and set these credentials locally, using the `bc.search.elasticsearch7` backend. An example of this configuration is in `bc/settings/local.py.example`.

## File storage

Does this use AWS S3? Via Buckup? Is it open to the public?

## DNS

## TLS/SSL/HTTPS

## Wagtail Transfer

This project uses [Wagtail Transfer](https://wagtail.github.io/wagtail-transfer/) to allow transferring content between the staging and production instance.

To enable the transfer between the instances, a few environment variables need to be defined.

If an instance is supposed to serve as a source (in our case the staging instance) for imports to another instance, you need to configure the `WAGTAILTRANSFER_SECRET_KEY`.
The `WAGTAILTRANSFER_SECRET_KEY` setting is used to authenticate the communication between the source and destination instances.
This environment variable only needs to be set on sources instances.

On the destination site, you need to configure `WAGTAILTRANSFER_SOURCE_KEY` and `WAGTAILTRANSFER_SOURCE_URL`.
`WAGTAILTRANSFER_SOURCE_KEY` on the destination instance needs to match the `WAGTAILTRANSFER_SECRET_KEY` used on the source instance.
E.g. if on the staging instance you have used `WAGTAILTRANSFER_SECRET_KEY="abc123"` (which is not recommended), then you would set `WAGTAILTRANSFER_SOURCE_KEY="abc123` on the production instance.

Additionally, you need to configure `WAGTAILTRANSFER_SOURCE_URL` on the destination instance, so it knows the endpoint to send its requests to.
E.g. on the `WAGTAILTRANSFER_SOURCE_URL="https://staging.example.com/wagtail-transfer/"`

Additionally, you can set the `WAGTAILTRANSFER_SOURCE_LABEL` on the destination instance.
`WAGTAILTRANSFER_SOURCE_LABEL` defines the name that will show up in the admin to select the source instance.
Use only valid Python variable names (i.e. no `-` is allowed.).
E.g. on the production instance you might want to set this to `"staging"`.

## Resetting the Staging site

Steps for resetting the `staging` git branch, and deploying it with a clone of the production site database.

### Pre-flight checks

1. Is this okay with the client, and other developers?
1. Is there any test content on staging that may need to be recreated, or be a reason to delay?
1. What branches are currently merged to staging?

   ```bash
   $ git branch -a --merged origin/staging > branches_on_staging.txt
   $ git branch -a --merged origin/master > branches_on_master.txt
   $ diff branches_on_{master,staging}.txt
   ```

   Take note if any of the above are stale, not needing to be recreated.

1. Are there any user accounts on staging only, which will need to be recreated? Check with the client, and record them.
1. Take a backup of staging
   ```bash
   $ heroku pg:backups:capture -a buckinghamshire-staging
   ```

### Git

1. Reset the staging branch
   ```bash
   $ git checkout staging && git fetch && git reset --hard origin/master && git push --force
   ```
1. Tell your colleagues
   > @here I have reset the staging branch. Please delete your local staging branches
   >
   > ```
   > $ git branch -D staging
   > ```
   >
   > to avoid accidentally merging in the old version
1. Force-push to Heroku, otherwise CI will later fail `$ git push --force heroku-staging master`
1. Merge in the relevant branches
   ```bash
   $ git merge --no-ff origin/feature/123-extra-spangles
   ```
1. Check for any newly necessary merge migrations `$ ./manage.py makemigrations --check`

### Database

1. List production database backups:
   ```bash
   $ heroku pg:backups -a buckinghamshire-production
   ```
1. Get a signed S3 URL of your chosen backup:
   ```bash
   $ heroku pg:backups:url {backup-name} -a buckinghamshire-production
   ```
1. Upload to staging:
   ```bash
   $ heroku pg:backups:restore {backup-url} DATABASE_URL -a buckinghamshire-staging
   ```
   This is a destructive action. Proofread it thoroughly.
1. Delete any personally-identifying data from staging. See [Data protection](data-protection.md) for instructions.

### Media

The fab commands are sufficient here. It's quicker just to copy original image files across (with no renditions):

```bash
$ fab pull-production-images
$ fab push-staging-images
```

…otherwise if you need everything, i.e. uploaded documents, images and renditions:

```bash
$ fab pull-production-media
$ fab push-staging-media
```

### Cleanup

1. Check the staging site loads
1. Update the Wagtail Site records, as the database will contain the production URLs
1. Check CI is working https://git.torchbox.com/buckinghamshire-council/bc/pipelines

### Comms

1. Inform the client of the changes.
   > - All user accounts have been copied across, so your old staging password will no longer work. Log in with your production password (and then change it), or use the 'forgot password' feature.
   > - Any test content has been reset. This is probably the biggest inconvenience. Sorry.
   > - I have deleted the personally-identifying data from form submissions and job alert subscriptions. If there's any more on production (there shouldn't be) then please let me know and I'll remove it from staging.
