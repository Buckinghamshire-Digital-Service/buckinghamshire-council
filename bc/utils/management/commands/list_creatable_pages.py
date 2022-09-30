from dataclasses import dataclass

from django.core.management.base import BaseCommand

from wagtail.models import get_page_models


@dataclass
class Result:
    page_id: int
    block_type: str


class Command(BaseCommand):
    help = "Print a nested list of page types and their creatable children"

    def handle(self, *args, **options):

        for model in get_page_models():
            if model.get_verbose_name() == "Page":
                # Don't include the bare Page model
                continue
            print(model.get_verbose_name())
            for child_type in model.creatable_subpage_models():
                print(f" - {child_type.get_verbose_name()}")
