from django.core.management.base import BaseCommand

from bc.service_directory import taxonomies
from bc.service_directory.models import ServiceDirectory


class Command(BaseCommand):
    help = "Fetch and create service directory taxonomies from the API"

    def handle(self, *args, **options) -> None:
        for directory in ServiceDirectory.objects.all():
            try:
                taxonomies.fetch_and_create_taxonomies(directory, api_timeout=60)
            except taxonomies.DirectoryIsNotEnabled:
                self.stdout.write(
                    self.style.WARNING(
                        f"Directory {directory.name} (PK={directory.pk}) is not enabled. Skipping."
                    )
                )
