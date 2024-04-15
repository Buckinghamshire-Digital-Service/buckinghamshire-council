from typing import List
from unittest import mock

import responses
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from requests import ReadTimeout, Response

from bc.area_finder.client import BucksMapsClient

fake = Faker("en_GB")

DISTRICT_AYLESBURY_VALE = "Aylesbury Vale District"
DISTRICT_CHILTERN = "Chiltern District"
DISTRICT_SOUTH_BUCKS = "South Bucks District"
DISTRICT_WYCOMBE = "Wycombe District"
DISTRICT_NAMES = [
    DISTRICT_AYLESBURY_VALE,
    DISTRICT_CHILTERN,
    DISTRICT_SOUTH_BUCKS,
    DISTRICT_WYCOMBE,
]


def get_feature(
    number: str, street: str, city: str, postcode: str, district_name: str
) -> dict:
    return {
        "attributes": {
            # UPRNs are unique, but we don't use them
            # "UPRN": 10003242839,
            "FULL_ADDRESS": ", ".join(
                [number, street, city, "Buckinghamshire", postcode]
            ),
            "NAME": district_name,
            # We don't use the CONTACT property
            # "CONTACT": "http://www.example.gov.uk/",
        },
        # geometry is included in the response, but we don't use it
        # "geometry": {"x": 491859.61000000034, "y": 190529.22000000067},
    }


def get_features(postcode: str, feature_count: int, districts: List[int]) -> List[dict]:
    street = fake.street_name()
    city = fake.city()
    return [
        get_feature(
            str(i + 1),
            street,
            city,
            postcode,
            districts[i % len(districts)],  # repeatedly loop over the list
        )
        for i in range(feature_count)
    ]


def get_response(features: List[dict]) -> dict:

    return {
        "objectIdFieldName": "OBJECTID_12",
        "globalIdFieldName": "",
        "geometryType": "esriGeometryPoint",
        "spatialReference": {"wkid": 27700, "latestWkid": 27700},
        "fields": [
            {"name": "UPRN", "alias": "UPRN", "type": "esriFieldTypeDouble"},
            {
                "name": "FULL_ADDRESS",
                "alias": "FULL_ADDRESS",
                "type": "esriFieldTypeString",
                "length": 1073741822,
            },
            {
                "name": "NAME",
                "alias": "NAME",
                "type": "esriFieldTypeString",
                "length": 60,
            },
            {
                "name": "CONTACT",
                "alias": "CONTACT",
                "type": "esriFieldTypeString",
                "length": 250,
            },
        ],
        "features": features,
    }


class FixturesTest(TestCase):
    """This tests the fixture utility functions.

    Test that the output of get_feature and get_response are suitable for unit testing
    the app.
    """

    def setUp(self):
        self.url = reverse("area_finder")
        self.api_client = BucksMapsClient()

    @responses.activate
    def test_format(self):
        features = get_features(
            "W1A 1AA", feature_count=1, districts=[DISTRICT_WYCOMBE]
        )
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(features),
        )
        resp = self.api_client.query_postcode("W1A 1AA")
        self.assertIsInstance(resp, Response)
        self.assertIsInstance(resp.json(), dict)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, BucksMapsClient.base_url)

    @responses.activate
    def test_unmatched_address(self):
        response = get_response(
            get_features(
                "W1A 1AA", feature_count=0, districts=[DISTRICT_AYLESBURY_VALE]
            )
        )
        self.assertEqual(len(response["features"]), 0)

    @responses.activate
    def test_single_address(self):
        response = get_response(
            get_features(
                "W1A 1AA", feature_count=1, districts=[DISTRICT_AYLESBURY_VALE]
            )
        )
        self.assertEqual(len(response["features"]), 1)

    @responses.activate
    def test_multiple_addresses_in_one_area(self):
        response = get_response(
            get_features("W1A 1AA", feature_count=10, districts=[DISTRICT_CHILTERN])
        )
        self.assertEqual(len(response["features"]), 10)
        areas = {feature["attributes"]["NAME"] for feature in response["features"]}
        self.assertEqual(len(areas), 1)

    @responses.activate
    def test_multiple_addresses_in_multiple_areas(self):
        response = get_response(
            get_features(
                "W1A 1AA",
                feature_count=10,
                districts=[DISTRICT_WYCOMBE, DISTRICT_CHILTERN, DISTRICT_SOUTH_BUCKS],
            )
        )
        self.assertEqual(len(response["features"]), 10)
        areas = {feature["attributes"]["NAME"] for feature in response["features"]}
        self.assertEqual(len(areas), 3)

    @responses.activate
    def test_querying_the_view_queries_the_api(self):
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(
                get_features(
                    "W1A 1AA", feature_count=5, districts=[DISTRICT_AYLESBURY_VALE]
                )
            ),
        )
        self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, BucksMapsClient.base_url)


class AreaFinderTest(TestCase):
    def setUp(self):
        self.url = reverse("area_finder")
        self.api_client = BucksMapsClient()

    def test_missing_postcode(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)

    def test_bad_postcode(self):
        resp = self.client.get(self.url + "?postcode=foo")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Please enter a valid postcode")

    @responses.activate
    def test_unmatched_postcode(self):
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(
                get_features("W1A 1AA", feature_count=0, districts=[]),
            ),
        )
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)
        self.assertEqual(
            json_response["error"], "Please enter a Buckinghamshire postcode."
        )

    @responses.activate
    def test_uniquely_mapped_postcode(self):
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(
                get_features(
                    "W1A 1AA", feature_count=5, districts=[DISTRICT_AYLESBURY_VALE]
                )
            ),
        )
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertEqual(json_response, {"area": "Aylesbury Vale"})

    @responses.activate
    def test_multiple_district_response(self):
        postcode = "W1A 1AA"
        street = "The Street"
        city = "Bofuki Nepoo"
        features = [
            get_feature("1", street, city, postcode, DISTRICT_AYLESBURY_VALE),
            get_feature("2", street, city, postcode, DISTRICT_CHILTERN),
            get_feature("3", street, city, postcode, DISTRICT_AYLESBURY_VALE),
            get_feature("4", street, city, postcode, DISTRICT_CHILTERN),
            get_feature("5", street, city, postcode, DISTRICT_WYCOMBE),
            get_feature("6", street, city, postcode, DISTRICT_WYCOMBE),
            get_feature("7", street, city, postcode, DISTRICT_SOUTH_BUCKS),
            get_feature("8", street, city, postcode, DISTRICT_SOUTH_BUCKS),
        ]
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(features),
        )
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("border_overlap_html", json_response)
        # NB the following is a list of lists, but in the view we assemble a list of
        # tuples. The process of returning a django.http.JsonResponse object, and then
        # examining resp.json(), munges this to a list of lists.
        self.assertEqual(
            json_response["addresses"],
            [
                [
                    "Aylesbury Vale",
                    "1, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA",
                ],
                ["Chiltern", "2, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA"],
                [
                    "Aylesbury Vale",
                    "3, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA",
                ],
                ["Chiltern", "4, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA"],
                ["Wycombe", "5, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA"],
                ["Wycombe", "6, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA"],
                [
                    "South Bucks",
                    "7, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA",
                ],
                [
                    "South Bucks",
                    "8, The Street, Bofuki Nepoo, Buckinghamshire, W1A 1AA",
                ],
            ],
        )

    @mock.patch("bc.area_finder.views.BucksMapsClient")
    def test_formatted_postcode_is_queried_from_api(self, mock_client):
        raw_postcode = "w1a1aa"
        formatted_postcode = "W1A 1AA"
        self.client.get(self.url + "?postcode=" + raw_postcode)
        mock_client().query_postcode.assert_called_once_with(formatted_postcode)

    @responses.activate
    def test_formatted_postcode_is_shown_to_user(self):
        raw_postcode = "w1a1aa"
        formatted_postcode = "W1A 1AA"
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json=get_response(
                get_features(
                    formatted_postcode,
                    feature_count=2,
                    districts=[DISTRICT_WYCOMBE, DISTRICT_SOUTH_BUCKS],
                )
            ),
        )
        resp = self.client.get(self.url + "?postcode=" + raw_postcode)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 200)
        json_response = resp.json()
        self.assertIn("border_overlap_html", json_response)
        # The formatted postcode is in the JSON
        self.assertIn("formatted_postcode", json_response)
        self.assertEqual(json_response["formatted_postcode"], formatted_postcode)
        # The formatted postcode is in the display text
        self.assertIn(formatted_postcode, json_response["border_overlap_html"])
        # And the user's input is not.
        self.assertNotIn(raw_postcode, json_response["border_overlap_html"])

    @responses.activate
    def test_error_response(self):
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json={"error": "some message"},
            status=400,
        )
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)

    @responses.activate
    def test_non_200_non_error_response(self):
        """Test non-200 responses that don't raise an error, and contain "error".

        In this case, the message from the API should be forwarded to the user.
        """
        responses.add(
            responses.POST,
            self.api_client.base_url,
            json={"error": "some message"},
            status=201,
        )
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "some message")

    @mock.patch("bc.area_finder.views.BucksMapsClient")
    def test_timeout(self, mock_client):
        mock_client().query_postcode.side_effect = ReadTimeout
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)

    @mock.patch("bc.area_finder.views.BucksMapsClient")
    def test_connectionerror(self, mock_client):
        mock_client().query_postcode.side_effect = ConnectionError
        resp = self.client.get(self.url + "?postcode=W1A+1AA")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers["content-type"], "application/json")
        json_response = resp.json()
        self.assertIn("error", json_response)
