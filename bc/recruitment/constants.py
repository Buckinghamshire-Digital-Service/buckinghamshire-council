JOB_FILTERS = [
    {
        "name": "category",
        "filter_key": "subcategory__categories__slug",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
    }
]

JOB_BOARD_DEFAULT = "external"
JOB_BOARD_CHOICES = [
    JOB_BOARD_DEFAULT,
    "internal",
]  # Must define corresponding TALENTLINK_API_USERNAME
