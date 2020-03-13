from django import template

from bc.recruitment.models import JobCategory

register = template.Library()


@register.inclusion_tag("patterns/molecules/search-filters/search-filters.html")
def jobs_search_filters(request, search_results, search_results_with_schools):
    job_categories = JobCategory.get_categories_summary(search_results).order_by(
        "label"
    )
    selected_categories = request.GET.getlist("category")
    hide_schools_and_early_years = request.GET.get(
        "hide_schools_and_early_years", False
    )

    return {
        "hide_schools_and_early_years": {
            "label": "Hide all schools and early years jobs",
            "count": JobCategory.schools_and_early_years_count(
                search_results_with_schools
            ),
            "selected": hide_schools_and_early_years,
        },
        "filters": [
            {
                "title": "More filtering options",
                "options": job_categories,
                "selected": selected_categories,
                "key": "category",
            }
        ],
    }
