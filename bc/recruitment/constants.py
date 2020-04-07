JOB_FILTERS = [
    {
        "name": "category",
        "filter_key": "subcategory__categories__slug",  # to use in Queryset Filter. Eg. 'subcategory__categories__slug'
    }
]

JOB_BOARD_CHOICES = ["external", "internal"]

JOB_BOARD_CHOICES_DEFAULT = "external"
