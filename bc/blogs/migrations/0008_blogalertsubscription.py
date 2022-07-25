# Generated by Django 3.2.9 on 2022-06-05 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0007_blogglobalhomepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogAlertSubscription",
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
                ("email", models.EmailField(max_length=254)),
                ("confirmed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "token",
                    models.CharField(editable=False, max_length=255, unique=True),
                ),
                (
                    "homepage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blogs.bloghomepage",
                    ),
                ),
            ],
        ),
    ]
