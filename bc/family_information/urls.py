from django.urls import path

from bc.family_information.views import get_corresponding_ehc_co, get_matching_schools

urlpatterns = [
    path("school/", get_matching_schools, name="get_matching_schools"),
    path(
        "ehcco/",
        get_corresponding_ehc_co,
        name="get_corresponding_ehc_co",
    ),
]

app_name = "family_information"
