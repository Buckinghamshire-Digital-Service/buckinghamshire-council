from django import template
from django.db.models import F

from wagtail.core.models import Site

from bc.recruitment.models import JobCategory, TalentLinkJob
from bc.recruitment.utils import get_school_and_early_years_count

register = template.Library()


@register.inclusion_tag("patterns/molecules/search-filters/search-filters.html")
def jobs_search_filters(request, unfiltered_results=None):
    search_postcode = request.GET.get("postcode", None)
    homepage = Site.find_for_request(request).root_page.specific

    if not unfiltered_results:
        # Provide a default queryset for Pattern Library
        unfiltered_results = TalentLinkJob.objects.filter(homepage=homepage).all()

    hide_schools_and_early_years = request.GET.get(
        "hide_schools_and_early_years", False
    )

    job_categories = JobCategory.get_categories_summary(
        unfiltered_results, homepage=homepage
    ).order_by("sort_order")

    return {
        "hide_schools_and_early_years": {
            "label": "Hide all schools and early years jobs",
            "count": get_school_and_early_years_count(unfiltered_results),
            "selected": hide_schools_and_early_years,
        },
        "filters": [
            {
                "title": "Job categories",
                "options": job_categories,
                "selected": request.GET.getlist("category"),
                "key": "category",
            },
            {
                "title": "Job subcategories",
                "options": unfiltered_results.values("subcategory__title")
                .annotate(key=F("subcategory__title"), label=F("subcategory__title"),)
                .order_by("subcategory__title")
                .distinct(),
                "selected": request.GET.getlist("subcategory"),
                "key": "subcategory",
            },
            {
                "title": "Contract type",
                "options": unfiltered_results.values("contract_type")
                .annotate(key=F("contract_type"), label=F("contract_type"))
                .order_by("contract_type")
                .distinct(),
                "selected": request.GET.getlist("contract"),
                "key": "contract",
            },
            {
                "title": "Working hours",
                "options": unfiltered_results.values("working_hours")
                .annotate(key=F("working_hours"), label=F("working_hours"),)
                .order_by("working_hours")
                .distinct(),
                "selected": request.GET.getlist("working_hours"),
                "key": "working_hours",
            },
            {
                "title": "Salary range",
                "options": unfiltered_results.exclude(salary_range__exact="")
                .values("salary_range")
                .annotate(key=F("salary_range"), label=F("salary_range"))
                .order_by("salary_range")
                .distinct(),
                "selected": request.GET.getlist("salary_range"),
                "key": "salary_range",
            },
        ],
        "search_postcode": search_postcode,
    }
