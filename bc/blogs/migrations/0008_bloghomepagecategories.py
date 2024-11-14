# Generated by Django 3.2.13 on 2022-07-11 19:49

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0007_blogglobalhomepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogHomePageCategories",
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
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("name", models.TextField()),
                ("slug", models.SlugField(editable=False)),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_categories",
                        to="blogs.bloghomepage",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="categories",
            field=modelcluster.fields.ParentalManyToManyField(
                related_name="related_posts", to="blogs.BlogHomePageCategories"
            ),
        ),
        migrations.AddConstraint(
            model_name="bloghomepagecategories",
            constraint=models.UniqueConstraint(
                fields=("page", "slug"), name="unique_page_slug"
            ),
        ),
    ]
