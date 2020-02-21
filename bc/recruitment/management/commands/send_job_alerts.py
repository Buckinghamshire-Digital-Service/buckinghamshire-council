import json

from django.core.management.base import BaseCommand
from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.timezone import now

from bc.recruitment.models import (
    JobAlertNotificationTask,
    JobAlertSubscription,
    TalentLinkJob,
)
from bc.recruitment.utils import get_jobs_search_results
from bc.utils.email import NotifyEmailMessage


class Command(BaseCommand):
    help = "Notifies job alert subscribers of new matches"

    def handle(self, *args, **options):
        start_time, end_time = self.get_times()
        queryset = self.get_queryset(start_time, end_time)
        task = JobAlertNotificationTask.objects.create(started=end_time)

        messages = []

        alerts = JobAlertSubscription.objects.filter(confirmed=True)
        for alert in alerts:
            search_params = json.loads(alert.search)
            querydict = QueryDict(mutable=True)
            querydict.update(search_params)
            results = get_jobs_search_results(querydict, queryset)

            if results:
                # TODO Add this when the unsubscription view is written
                # unsubscribe_url = reverse("alert_unsubscribe", args=[alert.token])
                subject = "New job search results"
                body = render_to_string(
                    "patterns/email/job_search_results_alert.txt",
                    context={
                        "results": results,
                        "search_term": alert.search,
                        # TODO Add this when the unsubscription view is written
                        # "unsubscribe_url": unsubscribe_url,
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

        self.stdout.write(f"{len(alerts)} subscriptions evaluated")
        self.stdout.write(f"{num_sent} emails sent")

    def get_times(self):
        # Set the search start date from the latest notification date
        try:
            start_time = (
                JobAlertNotificationTask.objects.filter(is_successful=True)
                .latest("started")
                .started
            )
        except JobAlertNotificationTask.DoesNotExist:
            start_time = None
        end_time = now()
        return start_time, end_time

    def get_queryset(self, start_time, end_time):
        params = {"created__lt": end_time}
        if start_time:
            params["created__gte"] = start_time
        return TalentLinkJob.objects.filter(**params)
