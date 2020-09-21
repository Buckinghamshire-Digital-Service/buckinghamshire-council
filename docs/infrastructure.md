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

## File storage

Does this use AWS S3? Via Buckup? Is it open to the public?

## DNS

## TLS/SSL/HTTPS

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
