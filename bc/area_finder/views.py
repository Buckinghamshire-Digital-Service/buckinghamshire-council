from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.html import escape

import requests
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes

from bc.area_finder.constants import BORDER_POSTCODES
from bc.area_finder.utils import (
    area_from_district,
    clean_escaped_html,
    validate_postcode,
)
from bc.utils.models import ImportantPages


@api_view(["GET"])
@authentication_classes([])
def area_finder(request):
    """
    Search for district council by postcode using the mapit.mysociety API
    https://mapit.mysociety.org/
    """
    if request.method != "GET" or not request.is_ajax():
        return JsonResponse(
            {"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not request.GET.get("postcode"):
        return JsonResponse(
            {"message": "Must specify a postcode."}, status=status.HTTP_200_OK
        )
    postcode = request.GET.get("postcode")
    try:
        formatted_postcode = validate_postcode(postcode)
    except ValidationError:
        error = "Postcode {} is not valid.".format(escape(postcode))
        return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST,)

    if formatted_postcode in BORDER_POSTCODES:
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
    # parameter `generation=38` keeps historic data on districts
    api_url = "https://mapit.mysociety.org/postcode/{}?api_key={}&generation=38".format(
        formatted_postcode, settings.MAPIT_API_KEY
    )
    response = requests.get(api_url, timeout=5)
    json_response = response.json()
    if response.status_code == 200:
        try:
            district_id = json_response["shortcuts"]["council"]["district"]
        except KeyError:
            return JsonResponse(
                {"message": "No area found for this postcode."},
                status=status.HTTP_200_OK,
            )
        except TypeError:
            # If postcode is not in Buckinghamshire
            if json_response["shortcuts"]["council"] == 2217:
                return JsonResponse(
                    {"error": "No area found for this postcode."},
                    status=status.HTTP_200_OK,
                )

            else:
                return JsonResponse(
                    {"error": "Please enter a Buckinghamshire postcode."},
                    status=status.HTTP_200_OK,
                )
        # If postcode is not in Buckinghamshire
        if json_response["shortcuts"]["council"]["county"] != 2217:
            return JsonResponse(
                {"error": "Please enter a Buckinghamshire postcode."},
                status=status.HTTP_200_OK,
            )

        try:
            district_name = json_response["areas"][str(district_id)]["name"]
            area_name = escape(area_from_district(district_name))
        except KeyError:
            return JsonResponse(
                {"message": "No area found for this postcode."},
                status=status.HTTP_200_OK,
            )
        html = (
            "<div data-response-text class='area-search__response-text'>"
            "<div>The postcode <strong>{}</strong> "
            "is in the <strong>{}</strong> area.".format(escape(postcode), area_name)
        )
        return JsonResponse(
            {"html": html, "area": area_name}, status=status.HTTP_200_OK
        )
    else:
        if json_response["error"]:
            error = json_response["error"]
            error = clean_escaped_html(escape(error))
            return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST,)
    return JsonResponse(
        {"message": "Request failed, try again"}, status=status.HTTP_400_BAD_REQUEST
    )
