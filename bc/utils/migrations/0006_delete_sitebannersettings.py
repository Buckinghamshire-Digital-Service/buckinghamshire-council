# Generated by Django 2.2.13 on 2020-07-08 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0005_add_cookie_important_page"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SiteBannerSettings",
        ),
    ]
