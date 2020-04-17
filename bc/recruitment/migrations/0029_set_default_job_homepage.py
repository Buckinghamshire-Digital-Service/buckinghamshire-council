from django.db import migrations


def set_default_job_homepage(apps, schema_editor):
    RecruitmentHomePage = apps.get_model("recruitment", "RecruitmentHomePage")
    home = RecruitmentHomePage.objects.first()

    TalentLinkJob = apps.get_model("recruitment", "TalentLinkJob")
    TalentLinkJob.objects.filter(homepage=None).update(homepage=home)

    JobAlertSubscription = apps.get_model("recruitment", "JobAlertSubscription")
    JobAlertSubscription.objects.filter(homepage=None).update(homepage=home)


class Migration(migrations.Migration):

    dependencies = [
        ("recruitment", "0028_add_job_board"),
    ]

    operations = [
        migrations.RunPython(
            set_default_job_homepage, reverse_code=migrations.RunPython.noop
        )
    ]
