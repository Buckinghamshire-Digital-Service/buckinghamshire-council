# Generated by Django 4.2.11 on 2024-06-20 13:07

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0014_systemmessagessettings_search_cta_button_and_more"),
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
