from django.core.management.base import BaseCommand
from tabulate import tabulate

from bc.cases.backends.respond.client import get_client


class Command(BaseCommand):
    help = "Lists Web Services defined in the Aptean Respond API"

    def handle(self, *args, **options):
        client = get_client()

        soup = client.get_fields()

        fields = []
        for field in soup.find_all("field"):
            schema_name = field.attrs["schema-name"]
            options = {"required": field.attrs["mandatory"] == "true"}
            fields.append((schema_name, options))

        self.stdout.write(
            tabulate(fields, headers=["SchemaName", "Options"], tablefmt="github")
        )

        self.stdout.write(self.style.SUCCESS("Done"))
