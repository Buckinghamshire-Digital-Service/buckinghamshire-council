# Generated by Django 4.0.10 on 2024-02-23 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0032_tableblock_help_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspagenewstype",
            name="news_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="news.newstype",
            ),
        ),
    ]
