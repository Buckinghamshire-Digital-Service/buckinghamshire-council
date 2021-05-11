from django.db import models

from wagtail.core import models as wt_models


class UsefulnessFeedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        wt_models.Page,
        on_delete=models.CASCADE,
        related_name="usefulness_feedback"
    )
    useful = models.BooleanField()


class FeedbackComment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        wt_models.Page,
        on_delete=models.CASCADE,
        related_name="feedback_comments"
    )
    action = models.CharField(
        verbose_name="What where you doing?",
        max_length=500,
    )
    issue = models.CharField(
        verbose_name="What went wrong?",
        max_length=500,
    )
