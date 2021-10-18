from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.html import escape

# import requests
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes

from bc.area_finder.client import BucksMapsClient
from bc.area_finder.utils import (
    area_from_district,
    clean_escaped_html,
    validate_postcode,
)
from bc.utils.models import ImportantPages


@api_view(["GET"])
@authentication_classes([])
def area_finder(request):
    """Map a postcode to a local area website, using maps.buckscc.gov.uk API"""
    postcode = request.GET.get("postcode")

    if not postcode:
        return JsonResponse(
            {"message": "Must specify a postcode."}, status=status.HTTP_200_OK
        )
    try:
        formatted_postcode = validate_postcode(postcode)
    except ValidationError:
        error = "Postcode {} is not valid.".format(escape(postcode))
        return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST,)

    client = BucksMapsClient()
    resp = client.query_postcode(formatted_postcode)

    json_response = resp.json()

    if resp.status_code != 200:
        if "error" in json_response:
            return JsonResponse(
                {"error": clean_escaped_html(escape(json_response["error"]))},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return JsonResponse(
            {"message": "Request failed, try again"}, status=status.HTTP_400_BAD_REQUEST
        )

    areas = {feature["attributes"]["NAME"] for feature in json_response["features"]}
    if not areas:
        return JsonResponse(
            {"error": "Please enter a Buckinghamshire postcode."},
            status=status.HTTP_200_OK,
        )

    if len(areas) > 1:
        contact_us_page = ImportantPages.for_request(request).contact_us_page
        if contact_us_page:
            contact_us_link = (
                f"<a href='{contact_us_page.url}'>contact our customer service "
                "centre.</a>"
            )
        else:
            contact_us_link = "contact our customer service centre."

        html = (
            "<div data-response-text class='area-search__response-text'>"
            f"<div>The postcode <strong>{escape(postcode)}</strong> is on the <strong>"
            "border between two areas.</strong></div><p>If you wish to know"
            f" the local area for your address, please {contact_us_link}"
            "</p></div>"
        )
        return JsonResponse({"border_overlap": html}, status=status.HTTP_200_OK)

    area_name = escape(area_from_district(areas.pop()))
    return JsonResponse({"area": area_name}, status=status.HTTP_200_OK)
