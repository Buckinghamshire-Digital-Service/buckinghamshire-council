from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document as WagtailDocument


class CustomDocument(AbstractDocument):
    talentlink_attachment_id = models.IntegerField(blank=True, null=True)
    admin_form_fields = WagtailDocument.admin_form_fields + (
        "talentlink_attachment_id",
    )
