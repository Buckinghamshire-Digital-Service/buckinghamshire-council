# Generated by Django 4.2.14 on 2024-11-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0036_eventindexpage_fetch_all_events"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventindexpage",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]