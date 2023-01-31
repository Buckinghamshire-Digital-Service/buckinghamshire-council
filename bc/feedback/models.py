from django.db import models

from wagtail import models as wt_models


class UsefulnessFeedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        wt_models.Page,
        null=True,
        on_delete=models.SET_NULL,
        related_name="usefulness_feedback",
    )
    original_url = models.URLField(max_length=2048)
    useful = models.BooleanField()

    def get_title(self):
        return self.page.title if self.page else "(deleted)"

    def get_current_url(self):
        return self.page.url if self.page else "(deleted)"


class FeedbackComment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(
        wt_models.Page,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feedback_comments",
    )
    original_url = models.URLField(max_length=2048)
    action = models.CharField(
        verbose_name="What were you doing?",
        max_length=500,
    )
    issue = models.CharField(
        verbose_name="What went wrong?",
        max_length=500,
    )

    def get_title(self):
        return self.page.title if self.page else "(deleted)"

    def get_current_url(self):
        return self.page.url if self.page else "(deleted)"
