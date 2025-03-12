from django.conf import settings

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class BucksMapsClient:
    """Python client for the upstream API maps.buckinghamshire.gov.uk.

    See documentation at docs/postcode-lookup.md.
    """

    base_url = (
        "https://maps.buckinghamshire.gov.uk"
        "/server/rest/services/BC/District_Postcode_Lookup/FeatureServer/0/query"
    )
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
        # Set up a session with retries for handling Sentry ConnectionError in production
        # for further information see documentation at docs/postcode-lookup.md
        self.session = Session()

        retries = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[502, 503, 504, 598],
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
