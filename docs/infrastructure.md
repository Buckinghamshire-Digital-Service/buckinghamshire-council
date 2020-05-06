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

What cache backend is used? What is it used for?

What front-end cache is there on production? How is it configured?

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
1. Take a backup of production
   ```bash
   $ heroku pg:backups:capture -a buckinghamshire-production
   ```
1. And staging `$ heroku pg:backups:capture -a buckinghamshire-staging`

### Git

1. Reset the branch
   ```bash
   $ git checkout master
   $ git pull
   $ git branch -D staging
   $ git push origin :staging
   $ git checkout -b staging
   $ git push --force --set-upstream origin staging
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

1. Duplicate the database from production to staging:
   ```bash
   $ heroku pg:copy buckinghamshire-production::DATABASE_URL DATABASE_URL -a buckinghamshire-staging
   ```
   This is a destructive action. Proofread it thoroughly.
1. Delete any personally-identifying data from staging. See [Data protection](data-protection.md) for instructions.

TODO: these steps do not currently use the Heroku backup from production; it would be better to.

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
