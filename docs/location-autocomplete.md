# Location autocomplete widget

Directory search widget streamfield block has a location autocomplete field.

The HTML template of the block can be found at
[bc/project_styleguide/templates/patterns/molecules/location-autocomplete/location-autocomplete.html](https://git.torchbox.com/buckinghamshire-council/bc/-/blob/release/bc/project_styleguide/templates/patterns/molecules/location-autocomplete/location-autocomplete.html).

The JavaScript component can be found at
[bc/static_src/javascript/components/location-autocomplete.js](https://git.torchbox.com/buckinghamshire-council/bc/-/blob/release/bc/static_src/javascript/components/location-autocomplete.js).

It uses Google Maps API to provide location suggestions: https://developers.google.com/maps/documentation/javascript/reference/places-autocomplete-service

## Configuration

It requires the `GOOGLE_MAPS_V3_APIKEY` environment variable to be configured. This settings is also used by different components on the website (e.g. [location maps widget](location-maps-widget.md)).
