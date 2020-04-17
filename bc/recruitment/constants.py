JOB_FILTERS = [
    {
        "name": "category",
        "filter_key": "subcategory__categories__slug",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
    },
    {
        "name": "subcategory",
        "filter_key": "subcategory__title",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
    },
    {"name": "contract", "filter_key": "contract_type"},
    {"name": "working_hours", "filter_key": "working_hours"},
    {"name": "salary_range", "filter_key": "salary_range"},
]
