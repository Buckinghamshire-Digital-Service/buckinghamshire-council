# Generated by Django 2.2.18 on 2021-06-09 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0004_feedback_original_url_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackcomment",
            name="action",
            field=models.CharField(max_length=500, verbose_name="What were you doing?"),
        ),
    ]
