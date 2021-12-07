from wagtail.core import hooks

from .models import StepByStepPage
from .utils import record_internal_links


@hooks.register("after_publish_page")
def update_internal_link_references(request, page):
    if isinstance(page.specific, StepByStepPage):
        record_internal_links(page)
