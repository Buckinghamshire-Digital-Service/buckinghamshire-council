# Generated by Django 2.2.10 on 2020-04-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0003_remove_web_service_definitonion_choices"),
    ]

    operations = [
        migrations.AddField(
            model_name="apteanrespondcaseformpage",
            name="show_live_chat_client",
            field=models.BooleanField(
                default=False, help_text="Show live chat support client on this page"
            ),
        ),
    ]
