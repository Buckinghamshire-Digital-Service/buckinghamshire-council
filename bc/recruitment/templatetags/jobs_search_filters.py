from django import template

from bc.recruitment.models import JobCategory, TalentLinkJob

register = template.Library()


@register.inclusion_tag("patterns/molecules/search-filters/search-filters.html")
def jobs_search_filters(request, search_results, search_results_with_schools):
    hide_schools_and_early_years = request.GET.get(
        "hide_schools_and_early_years", False
    )
    job_categories = JobCategory.get_categories_summary(search_results).order_by(
        "label"
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
                "selected": request.GET.getlist("category"),
                "key": "category",
            },
            {
                "title": "Working hours",
                "options": TalentLinkJob.get_working_hours_options(search_results),
                "selected": request.GET.getlist("working_hours"),
                "key": "working_hours",
            },
            # TODO: change to drop down?
            {
                "title": "Salary range",
                "options": TalentLinkJob.get_salary_range_options(search_results),
                "selected": request.GET.getlist("salary_range"),
                "key": "salary_range",
            },
        ],
    }
