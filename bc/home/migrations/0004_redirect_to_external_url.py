# Generated by Django 2.2.7 on 2020-01-13 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_homepage_hero"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="redirect_to",
            field=models.URLField(
                blank=True,
                help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                verbose_name="Redirect to external URL",
            ),
        ),
    ]
