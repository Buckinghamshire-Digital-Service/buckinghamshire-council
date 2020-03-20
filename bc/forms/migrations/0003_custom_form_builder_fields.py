# Generated by Django 2.2.10 on 2020-03-20 16:39

from django.db import migrations

import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0002_formpage_redirect_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="formfield",
            name="additional_text",
            field=wagtail.core.fields.RichTextField(
                blank=True, help_text="Rich text to display before the form field"
            ),
        ),
    ]
