from django import template

from bc.recruitment.models import JobCategory, TalentLinkJob
from bc.recruitment.utils import get_school_and_early_years_count

register = template.Library()


@register.inclusion_tag("patterns/molecules/search-filters/search-filters.html")
def jobs_search_filters(request, unfiltered_results=None):
    search_postcode = request.GET.get("postcode", None)
    job_board = request.site.root_page.specific.job_board

    if not unfiltered_results:
        # Provide a default queryset for Pattern Library
        unfiltered_results = TalentLinkJob.objects.filter(job_board=job_board).all()

    hide_schools_and_early_years = request.GET.get(
        "hide_schools_and_early_years", False
    )

    job_categories = JobCategory.get_categories_summary(
        unfiltered_results, job_board=job_board
    ).order_by("sort_order")

    return {
        "hide_schools_and_early_years": {
            "label": "Hide all schools and early years jobs",
            "count": get_school_and_early_years_count(unfiltered_results),
            "selected": hide_schools_and_early_years,
        },
        "filters": [
            {
                "title": "More filtering options",
                "options": job_categories,
                "selected": request.GET.getlist("category"),
                "key": "category",
            },
        ],
        "search_postcode": search_postcode,
    }
