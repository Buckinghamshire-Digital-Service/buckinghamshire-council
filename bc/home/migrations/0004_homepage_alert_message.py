# Generated by Django 2.2.7 on 2020-01-09 12:52

from django.db import migrations, models

import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_homepage_hero"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="alert_message",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="homepage",
            name="alert_title",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
