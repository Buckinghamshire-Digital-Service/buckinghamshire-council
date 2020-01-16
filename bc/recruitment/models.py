from django.db import models


class TalentLinkJob(models.Model):

    talentlink_id = models.IntegerField(unique=True)
    job_number = models.CharField(max_length=10, unique=True, blank=False)

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    category = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=255)
    closing_date = models.DateField()

    contact_email = models.EmailField()

    searchable_salary = models.CharField(
        max_length=255, help_text="Salary group for filtering"
    )
    searchable_location = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
    posting_start_date = models.DateTimeField()
    posting_end_date = models.DateTimeField()
    show_apply_button = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_number}: {self.title}"
