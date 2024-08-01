from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.html import escape

from requests import HTTPError, Timeout
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes

from bc.area_finder.client import BucksMapsClient
from bc.area_finder.utils import (
    area_from_district,
    clean_escaped_html,
    validate_postcode,
)


@api_view(["GET"])
@authentication_classes([])
def area_finder(request):
    """Map a postcode to a local area website, using maps.buckscc.gov.uk API"""
    postcode = request.GET.get("postcode")

    if not postcode:
        return JsonResponse(
            {"error": "Must specify a postcode."}, status=status.HTTP_200_OK
        )
    try:
        formatted_postcode = validate_postcode(postcode)
    except ValidationError:
        return JsonResponse(
            {"error": "Please enter a valid postcode"},
            status=status.HTTP_200_OK,
        )

    client = BucksMapsClient()

    try:
        resp = client.query_postcode(formatted_postcode)
    except (HTTPError, Timeout, ConnectionError):
        return JsonResponse(
            {"error": "Request failed, try again"}, status=status.HTTP_400_BAD_REQUEST
        )

    json_response = resp.json()

    if resp.status_code != 200:
        if "error" in json_response:
            return JsonResponse(
                {"error": clean_escaped_html(escape(json_response["error"]))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return JsonResponse(
            {"error": "Request failed, try again"}, status=status.HTTP_400_BAD_REQUEST
        )

    addresses = []
    areas = set()
    for feature in json_response["features"]:
        district = escape(area_from_district(feature["attributes"]["NAME"]))
        address = escape(feature["attributes"]["FULL_ADDRESS"])
        addresses.append((district, address))
        areas.add(feature["attributes"]["NAME"])

    if not areas:
        return JsonResponse(
            {"error": "Please enter a Buckinghamshire postcode."},
            status=status.HTTP_200_OK,
        )

    if len(areas) > 1:
        border_overlap_html = (
            f"<div>The postcode <strong>{escape(formatted_postcode)}</strong> is on "
            "the border between two areas. Select an address to help us redirect you "
            "to the right place.</div>"
        )
        return JsonResponse(
            {
                "border_overlap_html": border_overlap_html,
                "addresses": addresses,
                "formatted_postcode": formatted_postcode,
            },
            status=status.HTTP_200_OK,
        )

    area_name = escape(area_from_district(areas.pop()))
    return JsonResponse({"area": area_name}, status=status.HTTP_200_OK)
