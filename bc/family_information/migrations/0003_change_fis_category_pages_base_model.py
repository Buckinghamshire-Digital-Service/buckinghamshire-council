# Generated by Django 2.2.13 on 2020-11-02 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0003_job_employer_logo"),
        ("family_information", "0002_auto_20201027_0522"),
    ]

    operations = [
        migrations.AddField(
            model_name="categorytypeonepage",
            name="listing_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose the image you wish to be displayed when this page appears in listings",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="listing_summary",
            field=models.CharField(
                blank=True,
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="listing_title",
            field=models.CharField(
                blank=True,
                help_text="Override the page title used when this page appears in listings",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="redirect_to",
            field=models.URLField(
                blank=True,
                help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                verbose_name="Redirect to external URL",
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="show_live_chat_client",
            field=models.BooleanField(
                default=False, help_text="Show live chat support client on this page"
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="social_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
        migrations.AddField(
            model_name="categorytypeonepage",
            name="social_text",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="listing_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose the image you wish to be displayed when this page appears in listings",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="listing_summary",
            field=models.CharField(
                blank=True,
                help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="listing_title",
            field=models.CharField(
                blank=True,
                help_text="Override the page title used when this page appears in listings",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="redirect_to",
            field=models.URLField(
                blank=True,
                help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                verbose_name="Redirect to external URL",
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="show_live_chat_client",
            field=models.BooleanField(
                default=False, help_text="Show live chat support client on this page"
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="social_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
        migrations.AddField(
            model_name="categorytypetwopage",
            name="social_text",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
