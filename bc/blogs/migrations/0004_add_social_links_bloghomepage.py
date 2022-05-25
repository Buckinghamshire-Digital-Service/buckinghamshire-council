# Generated by Django 3.2.9 on 2022-05-25 11:15

import bc.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0003_featured_blogpost"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloghomepage",
            name="facebook_page_url",
            field=models.CharField(
                blank=True,
                max_length=255,
                validators=[bc.utils.validators.validate_facebook_domain],
            ),
        ),
        migrations.AddField(
            model_name="bloghomepage",
            name="linkedin_url",
            field=models.CharField(
                blank=True,
                max_length=255,
                validators=[bc.utils.validators.validate_linkedin_domain],
            ),
        ),
        migrations.AddField(
            model_name="bloghomepage",
            name="twitter_handle",
            field=models.CharField(
                blank=True,
                help_text="The Twitter username without the @, e.g. katyperry",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="bloghomepage",
            name="youtube_channel_url",
            field=models.URLField(
                blank=True, validators=[bc.utils.validators.validate_youtube_domain]
            ),
        ),
    ]
