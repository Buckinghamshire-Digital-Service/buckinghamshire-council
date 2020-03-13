JOB_FILTERS = [
    {
        "name": "category",
        "filter_key": "subcategory__categories__slug",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
    },
    {"name": "working_hours", "filter_key": "working_hours"},
    {"name": "salary_range", "filter_key": "searchable_salary"},
    # TODO: add contract_type (to model and API import)
]
