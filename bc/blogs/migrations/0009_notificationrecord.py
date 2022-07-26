# Generated by Django 3.2.9 on 2022-07-07 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0008_blogalertsubscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationRecord",
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
                ("was_sent", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "blog_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="blogs.blogpostpage",
                    ),
                ),
            ],
        ),
    ]