# Generated by Django 2.2.13 on 2020-07-08 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_add_show_live_chat_field"),
    ]

    operations = [
        migrations.RemoveField(model_name="homepage", name="alert_message",),
        migrations.RemoveField(model_name="homepage", name="alert_title",),
    ]