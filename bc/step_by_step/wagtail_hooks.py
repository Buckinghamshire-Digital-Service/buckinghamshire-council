from django.dispatch import receiver

from wagtail.signals import page_published

from .models import StepByStepPage
from .utils import record_internal_links


@receiver(page_published, sender=StepByStepPage)
def update_internal_link_references(instance, **kwargs):
    record_internal_links(instance)
