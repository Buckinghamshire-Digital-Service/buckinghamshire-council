from django.core.management.base import BaseCommand
from tabulate import tabulate

from bc.cases.backends.respond.client import get_client
from bc.cases.backends.respond.constants import CREATE_CASE_TYPE


class Command(BaseCommand):
    help = "Shows fields defined on CreateCase type services in the Aptean API"

    def handle(self, *args, **options):
        client = get_client()
        services = {}

        soup = client.get_web_service_meta_data()
        for webservice in soup.find_all("webservice"):
            name = webservice.find("name").text.strip()
            if webservice.attrs["type"] == CREATE_CASE_TYPE:
                services[name] = webservice

        self.stdout.write(self.style.NOTICE("Listed CreateCase type web services:"))
        for service_name in services.keys():
            self.stdout.write(f"- {service_name}")

        definition = input("Which one? ")

        service = services[definition]

        fields = []
        for xml_field in service.find_all("field"):
            fields.append(
                (
                    xml_field.find("name").text,
                    xml_field.attrs["schema-name"],
                    xml_field.attrs["data-type"],
                )
            )

        self.stdout.write(
            tabulate(
                fields, headers=["Name", "SchemaName", "data-type"], tablefmt="github"
            )
        )

        self.stdout.write(self.style.SUCCESS("Done"))
