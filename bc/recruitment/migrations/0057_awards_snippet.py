# Generated by Django 3.2.13 on 2023-02-01 11:09

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0056_jobcategory_icon"),
    ]

    operations = [
        migrations.CreateModel(
            name="AwardsSnippet",
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
                ("heading", models.CharField(max_length=255)),
                (
                    "awards",
                    wagtail.fields.StreamField(
                        [
                            (
                                "award",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(
                                                form_classname="full title",
                                                icon="title",
                                                label="Award title",
                                            ),
                                        ),
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "url",
                                            wagtail.blocks.URLBlock(required=False),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recruitmenthomepage",
            name="awards",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="recruitment.awardssnippet",
                verbose_name="Awards snippet",
            ),
        ),
    ]