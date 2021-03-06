# Generated by Django 2.2.10 on 2020-02-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0007_recruitmentindexpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobcategory",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                default="",
                help_text="The name of the category as it will appear in search filter e.g /search/category=[my-slug]",
                max_length=255,
            ),
            preserve_default=False,
        ),
    ]
