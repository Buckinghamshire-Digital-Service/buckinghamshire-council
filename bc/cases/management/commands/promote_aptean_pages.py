from django.core.management.base import BaseCommand
from tabulate import tabulate
from wagtail.blocks import StreamValue
from wagtail.contrib.redirects.models import Redirect

from bc.cases.models import (
    ApteanRespondCaseFormPage,
    ApteanRespondCaseFormPageRelatedPage,
)
from bc.standardpages.models import InformationPage


class Command(BaseCommand):
    help = "Tool to reorganise form pages which are children of information pages"

    def handle(self, *args, **options):
        for form_page in ApteanRespondCaseFormPage.objects.all():
            form_page.refresh_from_db()
            parent = form_page.get_parent(update=True).specific
            if not form_page.body and isinstance(parent, InformationPage):
                # Clone the parent body and related pages to the form page

                self.stdout.write(
                    tabulate(
                        [
                            (
                                page.id,
                                page.path,
                                page,
                                page.url,
                                page.get_children().count(),
                                (
                                    [
                                        block["value"]["text"]
                                        for block in page.body.stream_data
                                        if block["type"] == "button"
                                    ]
                                ),
                            )
                            for page in (parent, form_page)
                        ],
                        headers=[
                            "ID",
                            "Path",
                            "Title",
                            "URL",
                            "Children",
                            "Button blocks",
                        ],
                        tablefmt="github",
                    )
                )
                answer = input("Combine? y/n/q ")
                if answer.lower() != "y":
                    if answer.lower() == "q":
                        break
                    continue
                stream_data = self.map_stream_data(parent.body, form_page.id)
                form_page.body = StreamValue(
                    form_page._meta.get_field("body").stream_block,
                    stream_data,
                    is_lazy=True,
                )
                form_page.save()
                for related_page in parent.related_pages.all():
                    ApteanRespondCaseFormPageRelatedPage.objects.create(
                        source_page=form_page,
                        page=related_page.page,
                    )
                # Store the child and parent URLs for creating redirects
                old_form_page_url = form_page.url
                old_parent_page_url = parent.url
                # Promote the page to a sibling of its parent
                parent.slug = "renamed"
                parent.save()
                form_page.move(parent, "right")
                # Delete the parent page
                parent.delete()
                # Create permannet redirects
                form_page.refresh_from_db()
                Redirect.add_redirect(old_form_page_url, form_page)
                if form_page.url != old_parent_page_url:
                    Redirect.add_redirect(old_parent_page_url, form_page)

        self.stdout.write(self.style.SUCCESS("Done"))

    def map_stream_data(self, input_stream_value, form_page_id):
        raw_data = []
        for block in input_stream_value.raw_data:
            if (
                block["type"] == "button"
                and block["value"]["link_page"] == form_page_id
            ):
                raw_data.append(
                    {
                        "type": "form_link_button",
                        "value": {"text": block["value"]["text"]},
                    }
                )
            else:
                raw_data.append(block)
        return raw_data
