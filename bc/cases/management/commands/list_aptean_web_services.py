from django.core.management.base import BaseCommand

from bc.cases.backends.respond.client import get_client
from bc.cases.backends.respond.constants import CREATE_CASE_TYPE


class Command(BaseCommand):
    help = "Lists Web Services defined in the Aptean Respond API"

    def handle(self, *args, **options):
        client = get_client()

        self.stdout.write(self.style.NOTICE("All API-defined web services:"))
        soup = client.get_web_service_meta_data()
        for webservice in soup.find_all("webservice"):
            self.stdout.write(f"- {webservice.find('name').text.strip()}")

        self.stdout.write(
            self.style.NOTICE("Imported and registered CreateCase type web services:")
        )
        for service_name in client.services[CREATE_CASE_TYPE].keys():
            self.stdout.write(f"- {service_name}")

        self.stdout.write(self.style.NOTICE("Other registered web services:"))
        for service_name in client.services.keys():
            if service_name != CREATE_CASE_TYPE:
                self.stdout.write(f"- {service_name}")
        self.stdout.write(self.style.SUCCESS("Done"))
