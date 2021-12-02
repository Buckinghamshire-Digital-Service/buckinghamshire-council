from wagtail.core import hooks

from .models import StepByStepPage
from .utils import record_internal_links


@hooks.register("after_publish_page")
def update_internal_link_references(request, page):
    if request.method == "POST" and page.specific_class in [StepByStepPage]:
        record_internal_links(page)
