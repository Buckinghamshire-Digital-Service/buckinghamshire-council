from django import template

from bc.recruitment.models import JobCategory

register = template.Library()


@register.inclusion_tag("patterns/molecules/search-filters/search-filters.html")
def jobs_search_filters(request):
    job_categories = JobCategory.get_categories_summary().order_by("label")
    selected_categories = request.GET.getlist("category")

    return {
        "filters": [
            {
                "title": "Show only",
                "options": job_categories,
                "selected": selected_categories,
                "key": "category",
            }
        ],
    }
