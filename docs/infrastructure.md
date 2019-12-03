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
