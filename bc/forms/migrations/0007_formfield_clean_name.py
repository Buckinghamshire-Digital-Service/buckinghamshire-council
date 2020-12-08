# Generated by Django 2.2.17 on 2020-12-08 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0006_add_lookup_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="formfield",
            name="clean_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Safe name of the form field, the label converted to ascii_snake_case",
                max_length=255,
                verbose_name="name",
            ),
        ),
    ]
