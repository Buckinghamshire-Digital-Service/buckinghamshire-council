# Generated by Django 2.2.7 on 2019-12-05 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_customimage_file_hash"),
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="hero_image",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="strapline",
            field=models.CharField(
                help_text="eg. Welcome to Buckinghamshire", max_length=255
            ),
        ),
    ]
