from itertools import chain

from django.db import migrations

from bc.migration_utils.aligned_columns_data_migration import (
    alignedtypedtableblock_to_typedtableblock,
    typedtableblock_to_alignedtypedtableblock,
)
from bc.migration_utils.handlers import handle_page, handle_revision


def migrate(apps, mapper):
    InlineIndex = apps.get_model("inlineindex", "InlineIndex")
    InlineIndexChild = apps.get_model("inlineindex", "InlineIndexChild")

    longform_pages = InlineIndex.objects.all()
    chapter_pages = InlineIndexChild.objects.all()
    for page in chain(longform_pages, chapter_pages):
        handle_page(page, ["body"], mapper)

        for revision in page.revisions.all():
            handle_revision(revision, ["body"], mapper)


def forward(apps, schema):
    migrate(apps, typedtableblock_to_alignedtypedtableblock)


def backward(apps, schema):
    migrate(apps, alignedtypedtableblock_to_typedtableblock)


class Migration(migrations.Migration):

    dependencies = [
        ("inlineindex", "0024_add_aligned_columns"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
