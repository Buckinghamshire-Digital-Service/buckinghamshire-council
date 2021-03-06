# Generated by Django 2.2.13 on 2020-09-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_remove_alert_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="listing_summary",
            field=models.CharField(
                blank=True,
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
    ]
