# Generated by Django 2.2.10 on 2020-03-31 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0019_merge_20200325_1600"),
    ]

    operations = [
        migrations.AddField(
            model_name="talentlinkjob",
            name="location_lat",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
        migrations.AddField(
            model_name="talentlinkjob",
            name="location_lon",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
        migrations.AddField(
            model_name="talentlinkjob",
            name="location_postcode",
            field=models.CharField(blank=True, max_length=8),
        ),
    ]
