from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.search.backends import get_search_backend

from bc.family_information.models import School


class EHCCoChooserViewSet(ChooserViewSet):
    model = "family_information.EHCCo"

    icon = "user"
    choose_one_text = "Choose an EHC Co"
    choose_another_text = "Choose another EHC Co"
    edit_item_text = "Edit this EHC Co"
    form_fields = ["name", "email"]
    url_filter_parameters = ["name", "email"]


ehc_co_chooser_viewset = EHCCoChooserViewSet("ehc_co_chooser")


def get_matching_schools(request):
    q = request.GET.get("q", "")
    search_backend = get_search_backend()

    results = search_backend.autocomplete(q, School)

    return JsonResponse(
        [{"id": school.id, "text": school.name} for school in results],
        safe=False,
    )


def get_corresponding_ehc_co(request):
    school_id = request.GET.get("school_id", "")
    school = get_object_or_404(School, id=school_id)
    ehc_co = school.ehc_co
    if ehc_co:
        context = {
            "name": ehc_co.name,
            "email": ehc_co.email,
        }
    else:
        context = {
            "name": "TBC",
            "email": school.hub_email,
        }
    return JsonResponse(context)
