from django.core.management.base import BaseCommand
from wagtail.models import get_page_models


class Command(BaseCommand):
    help = "Print a nested list of page types and their creatable children"

    def handle(self, *args, **options):

        for model in get_page_models():
            if model.get_verbose_name() == "Page":
                # Describe the bare Page model more verbosely
                section_title = "Pages creatable at the site root"
            else:
                section_title = model.get_verbose_name()

            print(f" - {section_title}")
            for child_type in model.creatable_subpage_models():
                print(f"   - {child_type.get_verbose_name()}")
