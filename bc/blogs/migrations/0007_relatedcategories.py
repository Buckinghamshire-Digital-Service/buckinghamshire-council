# Generated by Django 3.2.9 on 2022-06-17 07:34

import django.db.models.deletion
from django.db import migrations, models

import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0007_blogglobalhomepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="RelatedCategories",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "source_page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_categories",
                        to="blogs.bloghomepage",
                    ),
                ),
                ("slug", models.SlugField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="relatedcategories",
            unique_together={("source_page", "slug")},
        ),
    ]
