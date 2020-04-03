# Generated by Django 2.2.10 on 2020-04-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_merge_20200117_1726"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="show_live_chat_client",
            field=models.BooleanField(
                default=False, help_text="Show live chat support client on this page"
            ),
        ),
    ]
