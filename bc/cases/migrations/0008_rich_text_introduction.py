# Generated by Django 2.2.12 on 2020-05-20 11:12

import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0007_remove_web_service_definition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apteanrespondcaseformpage",
            name="completion_title",
            field=models.CharField(
                help_text="Heading for the page shown after successful form submission.",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="apteanrespondcaseformpage",
            name="introduction",
            field=wagtail.fields.RichTextField(
                blank=True, help_text="Text displayed before the form"
            ),
        ),
    ]
