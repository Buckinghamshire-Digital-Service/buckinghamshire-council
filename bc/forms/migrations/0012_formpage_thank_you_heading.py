# Generated by Django 4.2.18 on 2025-03-12 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0011_formsubmission_formpage_auto_delete"),
    ]

    operations = [
        migrations.AddField(
            model_name="formpage",
            name="thank_you_heading",
            field=models.CharField(
                blank=True,
                help_text='The heading displayed above the <strong>Thank you text</strong>. Defaults to "Thank you".',
                max_length=200,
            ),
        ),
    ]
