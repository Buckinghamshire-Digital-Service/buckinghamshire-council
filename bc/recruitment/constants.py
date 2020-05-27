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

JOB_BOARD_DEFAULT = "external"
JOB_BOARD_CHOICES = [
    JOB_BOARD_DEFAULT,
    "internal",
]
# We must define corresponding TALENTLINK_API_USERNAME_{job_board} and
# TALENTLINK_APPLY_CONFIG_KEY_{job_board} in settings/base.py and env var.
