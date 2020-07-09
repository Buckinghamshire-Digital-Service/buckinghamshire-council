# Generated by Django 2.2.13 on 2020-06-18 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("utils", "0004_add_important_pages_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="importantpages",
            name="cookie_information_page",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.Page",
            ),
        ),
    ]