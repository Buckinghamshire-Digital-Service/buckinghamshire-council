from django.conf import settings

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class BucksMapsClient:
    """Python client for the upstream API maps.buckscc.gov.uk.

    See documentation at docs/postcode-lookup.md.
    """

    base_url = "https://maps.buckscc.gov.uk/arcgis/rest/services/Corporate/NLPG_Districts/FeatureServer/0/query"
    base_data = {
        "objectIds": "",
        "time": "",
        "geometry": "",
        "geometryType": "esriGeometryEnvelope",
        "inSR": "",
        "spatialRel": "esriSpatialRelIntersects",
        "distance": "",
        "units": "esriSRUnit_Foot",
        "relationParam": "",
        "outFields": "FULL_ADDRESS,NAME,CONTACT,UPRN",
        "returnGeometry": "true",
        "maxAllowableOffset": "",
        "geometryPrecision": "",
        "outSR": "",
        "gdbVersion": "",
        "returnDistinctValues": "false",
        "returnIdsOnly": "false",
        "returnCountOnly": "false",
        "returnExtentOnly": "false",
        "orderByFields": "FULL_ADDRESS",
        # "orderByFields": "",
        "groupByFieldsForStatistics": "",
        "outStatistics": "",
        "returnZ": "false",
        "returnM": "false",
        "multipatchOption": "",
        "resultOffset": "",
        "resultRecordCount": "",
        "f": "pjson",
    }

    def _post(self, data):
        """
        Set up a session with retries for handling Sentry ConnectionError in production.

        - `backoff_factor`: Increase in sleep time between retries (10%).
        - `status_forcelist`: List of status codes to retry on.
        - `allowed_methods`: Set of uppercased HTTP method verbs for retries.

        Retry the request 3 times with an increasing delay if it fails with a 598 error.
        """
        self.session = Session()

        retries = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[598],
            allowed_methods={"POST"},
        )

        self.session.mount(self.base_url, adapter=HTTPAdapter(max_retries=retries))

        response = self.session.post(
            self.base_url,
            data=data,
            timeout=settings.BUCKS_MAPS_CLIENT_API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response

    def query_postcode(self, postcode):
        data = self.base_data
        data["where"] = (f"POSTCODE = '{postcode}'",)
        return self._post(data)
