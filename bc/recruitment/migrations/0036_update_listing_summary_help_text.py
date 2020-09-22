# Generated by Django 2.2.13 on 2020-09-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0035_add_detail_to_storyblock"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruitmenthomepage",
            name="listing_summary",
            field=models.CharField(
                blank=True,
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="recruitmentindexpage",
            name="listing_summary",
            field=models.CharField(
                blank=True,
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
    ]
