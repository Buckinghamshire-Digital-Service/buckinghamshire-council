# Generated by Django 2.2.17 on 2021-03-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="alert_level",
            field=models.SmallIntegerField(
                choices=[(1, "Alert 1"), (2, "Alert 2"), (3, "Alert 3")],
                default=2,
                help_text="With Alert 1 as the highest alert",
            ),
        ),
    ]
