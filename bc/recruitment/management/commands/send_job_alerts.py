import json

from django.core.management.base import BaseCommand
from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.timezone import now

from bc.recruitment.models import (
    JobAlertNotificationTask,
    JobAlertSubscription,
    RecruitmentHomePage,
    TalentLinkJob,
)
from bc.recruitment.utils import get_job_search_results
from bc.utils.email import NotifyEmailMessage


class Command(BaseCommand):
    """This checks job alert subscriptions, and sends messages about new matches.

    Any further documentation for this feature is at docs/recruitment_site.md
    """

    help = "Notifies job alert subscribers of new matches"

    def handle(self, *args, **options):
        task = JobAlertNotificationTask.objects.create()
        try:
            start_time = (
                JobAlertNotificationTask.objects.filter(is_successful=True)
                .latest("started")
                .started
            )
        except JobAlertNotificationTask.DoesNotExist:
            start_time = None

        for homepage in RecruitmentHomePage.objects.live().all():
            messages = []
            alerts = JobAlertSubscription.objects.filter(
                confirmed=True, homepage=homepage
            )
            for alert in alerts:
                search_params = json.loads(alert.search)
                querydict = QueryDict(mutable=True)
                querydict.update(search_params)
                results = get_job_search_results(
                    querydict=querydict,
                    homepage=homepage,
                    queryset=self.get_queryset(
                        start_time=max(filter(None, [start_time, alert.created])),
                        end_time=task.started,
                    ),
                )

                if results:
                    subject = "New job search results"
                    body = render_to_string(
                        "patterns/email/job_search_results_alert.txt",
                        context={
                            "site_url": alert.site_url,
                            "results": results,
                            "search_term": alert.search,
                            "unsubscribe_url": alert.unsubscribe_url,
                        },
                    )
                    messages.append(
                        NotifyEmailMessage(subject=subject, body=body, to=[alert.email])
                    )

            num_sent = 0
            for message in messages:
                message.send()
                num_sent += 1

            task.is_successful = True
            task.ended = now()
            task.save()

            self.stdout.write(
                f"{len(alerts)} subscriptions for job site (id={homepage.id}) evaluated"
            )
            self.stdout.write(f"{num_sent} emails sent")

    def get_queryset(self, start_time, end_time):
        params = {"created__lt": end_time}
        if start_time:
            params["created__gte"] = start_time

        return TalentLinkJob.objects.filter(**params)
