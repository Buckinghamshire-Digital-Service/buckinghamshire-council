# Generated by Django 2.2.18 on 2021-02-17 09:55

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0008_systemmessagessettings_body_no_search_results"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemmessagessettings",
            name="search_input_help_text",
            field=wagtail.fields.RichTextField(
                blank=True,
                help_text="This text will appear below the input field on the search page. You can use it to direct the users or suggest other pages where to find information.",
                null=True,
                verbose_name="Search Input Help Text",
            ),
        ),
    ]
