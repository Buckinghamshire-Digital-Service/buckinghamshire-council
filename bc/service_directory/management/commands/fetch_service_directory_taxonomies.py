from django.core.management.base import BaseCommand

from bc.service_directory import taxonomies
from bc.service_directory.models import DirectoryManagementAPI


class Command(BaseCommand):
    help = "Fetch and create service directory taxonomies from the API"

    def handle(self, *args, **options) -> None:
        for management_api in DirectoryManagementAPI.objects.enabled().iterator():
            try:
                taxonomies.fetch_and_create_taxonomies(management_api, api_timeout=60)
            except taxonomies.DirectoryManagementAPIIsNotEnabled:
                self.stdout.write(
                    self.style.WARNING(
                        f'Directory Management API "{management_api.admin_name}" (PK={management_api.pk}) '
                        "is not enabled. Skipping."
                    )
                )
