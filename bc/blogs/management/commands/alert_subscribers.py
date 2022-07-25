import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from bc.blogs.models import NotificationRecord
from bc.blogs.utils import alert_subscribed_users

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Notify subscribed users of newly published blog posts"

    def handle(self, *args, **options):
        with transaction.atomic():
            pending_notifications = NotificationRecord.objects.select_for_update(
                skip_locked=True
            ).filter(was_sent=False)
            if pending_notifications:
                for record in pending_notifications:
                    alert_subscribed_users(record.blog_post_id)
                    record.was_sent = True
                    record.save()
            else:
                self.stdout.write(
                    "There are no pending subscription alert notifications"
                )
