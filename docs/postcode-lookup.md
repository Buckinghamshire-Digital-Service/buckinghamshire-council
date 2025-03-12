# Location based lookup

The site integrates with a Buckinghamshire Council geolocation API to determine what legacy council websites provide information for a user based on their address.

## Buckinghamshire Council mapping tool

This is a tool hosted at maps.buckinghamshire.gov.uk, built by exporting from the council's gazetteer into a geospatial database.

No authentication is required to query this API.

This is used By the LocalAreaLinksBlock StreamField block to match a submitted postcode to one of the four areas of Buckinghamshire Council, matching those served by the former district councils. A postcode query returns a list of street addresses, and a corresponding 'District Council' parameter.

If all the results for a query match a single district council (most queries), we redirect the user to the correct site. Otherwise we ask the user to give their street address.

## Configuration

The Python client is at `bc.area_finder.client.BucksMapsClient`. The timeout for the upstream API can be configured with the environment variable:

- `BUCKS_MAPS_CLIENT_API_TIMEOUT_SECONDS` (must be parsable as a `float`; defaults to `10`)
- Retries are implemented to handle a Sentry ConnectionError see in production.
  - `backoff_factor`: Increase in sleep time between retries (10%).
  - `status_forcelist`: List of status codes to retry on.
  - `allowed_methods`: Set of uppercased HTTP method verbs for retries.
