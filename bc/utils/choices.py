from django.db import models


class IconChoice(models.TextChoices):
    SCHOOL = "school", "School"
    SOCIAL = "social", "Social"
    COMMUNITIES = "communities", "Communities"
    TRANSPORT = "transport", "Transport"
    CORPORATE = "corporate", "Corporate"
    PARTNERS = "partners", "Partners"
    OTHER = "other", "Other"
