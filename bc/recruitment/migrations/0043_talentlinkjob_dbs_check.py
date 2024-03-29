# Generated by Django 2.2.21 on 2021-07-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0042_heading_subheading_helptext"),
    ]

    operations = [
        migrations.AddField(
            model_name="talentlinkjob",
            name="dbs_check",
            field=models.BooleanField(
                default=False, verbose_name="Does this role require a DBS check?"
            ),
        ),
    ]
