# Generated by Django 3.2.13 on 2022-09-27 09:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("wagtailcore", "0069_log_entry_jsonfield"),
        ("wagtailforms", "0005_alter_formsubmission_form_data"),
        ("wagtailredirects", "0008_add_verbose_name_plural"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("utils", "0011_wagtail_3_upgrade"),
        ("images", "0004_wagtail_3_upgrade"),
        ("feedback", "0005_feedback_field_label"),
        ("step_by_step", "0006_wagtail_3_upgrade"),
        ("wagtailsearchpromotions", "0002_capitalizeverbose"),
        ("forms", "0008_wagtail_3_upgrade"),
        ("alerts", "0003_alter_alert_content"),
        ("family_information", "0003_change_fis_category_pages_base_model"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FamilyInformationHomePage",
            new_name="SubsiteHomePage",
        ),
    ]
