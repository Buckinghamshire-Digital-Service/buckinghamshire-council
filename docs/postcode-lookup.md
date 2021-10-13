# Location based lookup

The site integrates with a Buckinghamshire Council geolocation API to determine what legacy council websites provide information for a user based on their address.

## Buckinghamshire Council mapping tool

This is a tool hosted at maps.buckscc.gov.uk, built by exporting from the council's gazetteer into a geospatial database.

There is an HTML interface for testing available at https://maps.buckscc.gov.uk/arcgis/rest/services/Corporate/NLPG_Districts/FeatureServer/0/query?where=POSTCODE+%3D+%27HP20+1UY%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&gdbVersion=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=&resultOffset=&resultRecordCount=&f=html. No authentication is required to query this API.

This is used By the LocalAreaLinksBlock StreamField block to match a submitted postcode to one of the four areas of Buckinghamshire Council, matching those served by the former district councils. A postcode query returns a list of street addresses, and a corresponding 'District Council' parameter.

If all the results for a query match a single district council (most queries), we redirect the user to the correct site. Otherwise we ask the user to give their street address.
