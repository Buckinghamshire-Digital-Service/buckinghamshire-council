# Generated by Django 2.2.12 on 2020-05-12 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_job_employer_logo'),
        ('family_information', '0005_auto_20200512_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='familyinformationhomepage',
            name='links_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
    ]
