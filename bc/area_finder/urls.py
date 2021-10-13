from django.urls import path

from bc.area_finder.views import area_finder

urlpatterns = [
    path("", area_finder, name="area_finder"),
]
