# Generated by Django 2.2.10 on 2020-04-01 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_customimage_file_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="customimage",
            name="talentlink_image_id",
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
