# Generated by Django 2.2.12 on 2020-05-12 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("family_information", "0003_auto_20200512_2333"),
    ]

    operations = [
        migrations.AlterField(
            model_name="familyinformationhomepage",
            name="left_lede",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="familyinformationhomepage",
            name="right_lede",
            field=models.TextField(null=True),
        ),
    ]
