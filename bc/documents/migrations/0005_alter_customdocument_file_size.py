# Generated by Django 4.2.18 on 2025-01-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0004_job_attachments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customdocument",
            name="file_size",
            field=models.PositiveBigIntegerField(editable=False, null=True),
        ),
    ]
