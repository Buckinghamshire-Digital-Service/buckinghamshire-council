from django.conf import settings
from django.core.management.base import BaseCommand

from bc.cases.backends.respond.client import get_client


class Command(BaseCommand):
    help = "Lists Web Services defined in the Aptean Respond API"

    def handle(self, *args, **options):
        client = get_client()

        soup = client.get_web_service_meta_data()

        found_service_names = {
            webservice.find("name").text.strip()
            for webservice in soup.find_all("webservice")
        }

        expected_create_case_services = {
            settings.RESPOND_COMPLAINTS_WEBSERVICE,
            settings.RESPOND_FOI_WEBSERVICE,
            settings.RESPOND_SAR_WEBSERVICE,
            settings.RESPOND_COMMENTS_WEBSERVICE,
            settings.RESPOND_COMPLIMENTS_WEBSERVICE,
            settings.RESPOND_DISCLOSURES_WEBSERVICE,
        }
        found_create_case_services = found_service_names & expected_create_case_services
        other_found_services = found_service_names - expected_create_case_services

        self.stdout.write(self.style.NOTICE("All API-defined create case services:"))
        for service_name in found_create_case_services:
            self.stdout.write(f"- {service_name}")

        self.stdout.write(self.style.NOTICE("Other API-reported web services:"))
        for service_name in other_found_services:
            self.stdout.write(f"- {service_name}")
        self.stdout.write(self.style.SUCCESS("Done"))
