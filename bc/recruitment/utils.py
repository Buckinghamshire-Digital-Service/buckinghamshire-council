import json

from django import forms
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin

from wagtail.core.models import Site

import requests

from bc.recruitment.constants import JOB_FILTERS
from bc.recruitment.models import JobCategory, RecruitmentHomePage, TalentLinkJob


def is_recruitment_site(request):
    return isinstance(
        Site.find_for_request(request).root_page.specific, RecruitmentHomePage
    )


def get_current_search(querydict):
    """
    Returns search query and filters in request.GET as json string
    """
    search = {}

    if querydict.get("query", None):
        search["query"] = querydict["query"]

    if querydict.get("postcode", None):
        search["postcode"] = querydict["postcode"]

    # Loop through our filters so we don't just store any query params
    for filter in JOB_FILTERS:
        selected = querydict.getlist(filter["name"])
        if selected:
            selected = list(dict.fromkeys(selected))  # Remove duplicate options
            search[filter["name"]] = sorted(selected)  # Sort options alphabetically

    return json.dumps(search)


def get_job_search_results(querydict, homepage, queryset=None):
    if queryset is None:
        queryset = TalentLinkJob.objects.all()

    queryset = queryset.filter(homepage=homepage)

    search_query = querydict.get("query", None)

    if search_query:
        vector = (
            SearchVector("title", weight="A")
            + SearchVector("job_number", weight="A")
            # + SearchVector("short_description", weight="A")
            + SearchVector("location", weight="B")
            + SearchVector("description", weight="C")
        )
        query = SearchQuery(search_query, search_type="phrase")
        search_results = (
            queryset.annotate(rank=SearchRank(vector, query))
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

    else:
        # Order by newest job at top
        search_results = queryset.order_by("posting_start_date")

    # Process 'hide schools and early years job'
    if querydict.get("hide_schools_and_early_years", False):
        schools_and_early_years_categories = (
            JobCategory.get_school_and_early_years_categories()
        )
        search_results = search_results.exclude(
            subcategory__categories__slug__in=schools_and_early_years_categories
        )

    # Process filters
    for filter in JOB_FILTERS:
        # QueryDict.update() used in send_job_alerts.py adds the values as list instead of multivalue dict.
        if isinstance(querydict.get(filter["name"]), list):
            selected = querydict.get(filter["name"])
        else:
            selected = querydict.getlist(
                filter["name"]
            )  # will return empty list if not found

        try:
            selected = [forms.CharField().clean(value) for value in selected]
        except ValidationError:
            # Abort any invalid string literals, e.g. SQL injection attempts
            continue

        if selected:
            search_results = search_results.filter(
                **{
                    filter["filter_key"] + "__in": selected
                }  # TODO: make case insensitive
            )

    # Process postcode search
    search_postcode = querydict.get("postcode", None)
    if search_postcode:
        postcode_response = requests.get(
            "https://api.postcodes.io/postcodes/" + search_postcode
        )
        if postcode_response.status_code == 200:
            postcode_response_json = postcode_response.json()
            search_lon = postcode_response_json["result"]["longitude"]
            search_lat = postcode_response_json["result"]["latitude"]

            search_results = search_results.annotate(
                distance=GetDistance(search_lat, search_lon)
            ).order_by("distance")

            if search_query:
                # Rank is only used when there is a search query
                search_results = search_results.order_by("distance", "-rank")

    return search_results


def GetDistance(point_latitude, point_longitude):
    # Calculate distance. See https://www.thutat.com/web/en/programming-and-tech-stuff/
    # web-programming/postgres-query-with-gps-distance-calculations-without-postgis/
    distance = (
        ACos(
            Sin(Radians(F("location_lat"))) * Sin(Radians(point_latitude))
            + Cos(Radians(F("location_lat")))
            * Cos(Radians(point_latitude))
            * Cos(Radians(F("location_lon") - point_longitude))
        )
        * 6371
        * 1000
    )

    return distance


def get_school_and_early_years_count(search_results):
    schools_and_early_years_categories = (
        JobCategory.get_school_and_early_years_categories()
    )
    if len(schools_and_early_years_categories):
        search_results = search_results.filter(
            subcategory__categories__slug__in=schools_and_early_years_categories
        )

    return len(search_results)
