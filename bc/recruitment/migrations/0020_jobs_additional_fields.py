# Generated by Django 2.2.10 on 2020-03-27 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0019_merge_20200325_1600"),
    ]

    operations = [
        migrations.AddField(
            model_name="talentlinkjob",
            name="contract_type",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
