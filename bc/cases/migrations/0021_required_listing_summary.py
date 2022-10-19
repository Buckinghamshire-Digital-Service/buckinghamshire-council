# Generated by Django 3.2.13 on 2022-10-07 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0020_wagtail_3_upgrade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apteanrespondcaseformpage",
            name="listing_summary",
            field=models.CharField(
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
    ]
