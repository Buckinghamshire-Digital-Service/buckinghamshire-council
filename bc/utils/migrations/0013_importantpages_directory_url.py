# Generated by Django 3.2.13 on 2023-03-06 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0012_sort_collections_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="importantpages",
            name="directory_url",
            field=models.URLField(
                blank=True,
                help_text="URL to the directory page (meant to be used by CAB and FIS sites).",
            ),
        ),
    ]
