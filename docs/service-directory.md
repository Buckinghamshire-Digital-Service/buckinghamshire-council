Service directory API is used to provide a list of services available.

This is used on the Directory Services StreamField block on location pages.

The directories are external systems that provide a list of services available in the area,
for example: https://directory.familyinfo.buckinghamshire.gov.uk/. We built the streamfield
block to output some of that data on the Wagtail website.

The data fetched from the API is:

- Taxonomy (the categories)
- Services (the activities)

Data is fetched from two separate API endpoints:

- Services are fetched from the specific directory endpoint,
  for example: `https://api.familyinfo.buckinghamshire.gov.uk/`.
- Taxonomy options are fetched from the directory management endpoint,
  for example: `https://manage-directory-listing.buckinghamshire.gov.uk/api/v1/taxonomies`.

Those API endpoints are public. If we hit rate limiting errors, the supplier can provide us with a private token.

Those APIs are not managed by Torchbox.

## Taxonomy fetch

Taxonomy fetch happens on a schedule using a management command. That needs to be set up on Heroku scheduler or equivalent.

```sh
 ./manage.py fetch_service_directory_taxonomies
```

## Services fetch

Services are fetched by Directory Services StreamField block on location pages.

That is done on the view when the page request happens.

## API data parsing and validation

Parsing and validation is done using https://github.com/lidatong/dataclasses-json/. Expect to see validation error exceptions if API shape changes.

## Configuration
The API endpoints are configured in Wagtail admin under "Service directory" -> "Directories" and "Service directory" -> "Management APIs".
