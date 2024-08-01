from django.core.management.base import BaseCommand

from tabulate import tabulate

from bc.cases.backends.respond.client import get_client
from bc.cases.backends.respond.constants import CUSTOM_OPTIONS


class Command(BaseCommand):
    help = "Lists Web Services defined in the Aptean Respond API"

    def handle(self, *args, **options):
        client = get_client()

        soup = client.get_categories()
        fields = []
        for field in soup.find_all("field"):
            schema_name = field.attrs["schema-name"]
            choices = [
                self.get_option_label(schema_name, o)
                for o in field.find_all("option")
                if o.attrs["available"] == "true"
            ]
            for i, (k, v) in enumerate(choices):
                if i == 0:
                    field_name = schema_name
                else:
                    field_name = ""
                fields.append((field_name, k, v))

        self.stdout.write(
            tabulate(fields, headers=["SchemaName", "key", "value"], tablefmt="github")
        )

        self.stdout.write(self.style.SUCCESS("Done"))

    def get_option_label(self, schema_name, option_xml):
        provided_label = option_xml.find("name").text.strip()
        try:
            label = CUSTOM_OPTIONS[schema_name][provided_label]
        except KeyError:
            label = provided_label
        return (option_xml.attrs["id"], label)
