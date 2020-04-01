# Generated by Django 2.2.10 on 2020-04-01 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_customimage_file_hash"),
        ("recruitment", "0024_merge_20200331_1816"),
    ]

    operations = [
        migrations.AddField(
            model_name="talentlinkjob",
            name="logo",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.CustomImage",
            ),
        ),
    ]
