from django.db import models

from wagtail.core import models as wt_models


class UsefulnessFeedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(wt_models.Page, on_delete=models.CASCADE, related_name="usefulness_feedback")
    useful = models.BooleanField()
