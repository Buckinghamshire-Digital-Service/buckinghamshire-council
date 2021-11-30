import requests


class BucksMapsClient:
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
        return requests.post(self.base_url, data=data)

    def query_postcode(self, postcode):
        data = self.base_data
        data["where"] = (f"POSTCODE = '{postcode}'",)
        return self._post(data)
