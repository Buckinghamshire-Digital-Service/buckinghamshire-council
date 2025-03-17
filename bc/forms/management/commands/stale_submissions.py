from django.core.management.base import BaseCommand
from django.template.defaultfilters import pluralize as pluralise

from bc.forms.models import FormSubmission


class Command(BaseCommand):
    help = "List stale form submissions"

    def add_arguments(self, parser):
        parser.add_argument("--delete", "-d", action="store_true")

    def handle(self, *args, **options):
        queryset = FormSubmission.objects.stale()
        if options["delete"]:
            deleted, _ = queryset.delete()
            msg = f"{deleted} submission{pluralise(deleted)} deleted successfully"
            self.stdout.write(msg)
        else:
            deleted = queryset.count()
            self.stdout.write(
                f"There {pluralise(deleted, 'is,are')} {deleted} stale submission{pluralise(deleted)}."
            )
            self.stdout.write("Run the command again with --delete to delete them.")
