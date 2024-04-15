import re

from django.db import transaction
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.models import Page

from .models import StepByStepReference

FIND_INTERNAL_LINK = re.compile(r'<a id="(\d+)" linktype="page">')


def step_by_step_page_changed(page_ids):
    # Find all the live pages to purge
    batch = PurgeBatch()
    for page in Page.objects.filter(pk__in=page_ids).live():
        batch.add_page(page)

    batch.purge()


def record_internal_links(page):
    steps = page.steps
    linked_pages = []
    for step in steps:
        information = step.value["information"].source
        linked_pages = linked_pages + FIND_INTERNAL_LINK.findall(information)
    linked_pages = set(linked_pages)
    references_to_create = [
        StepByStepReference(step_by_step_page=page, referenced_page_id=page_id)
        for page_id in linked_pages
    ]
    with transaction.atomic():
        StepByStepReference.objects.filter(step_by_step_page=page).delete()
        StepByStepReference.objects.bulk_create(references_to_create)

    step_by_step_page_changed(linked_pages)
