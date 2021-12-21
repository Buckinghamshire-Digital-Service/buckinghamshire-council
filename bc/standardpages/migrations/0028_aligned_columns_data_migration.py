from django.db import migrations

from bc.migration_utils.aligned_columns_data_migration import (
    alignedtypedtableblock_to_typedtableblock,
    typedtableblock_to_alignedtypedtableblock,
)
from bc.migration_utils.handlers import handle_page, handle_revision


def migrate(apps, mapper):
    InformationPage = apps.get_model("standardpages", "InformationPage")

    pages = InformationPage.objects.all()
    for page in pages:
        handle_page(page, ["body"], mapper)

        for revision in page.revisions.all():
            handle_revision(revision, ["body"], mapper)


def forward(apps, schema):
    migrate(apps, typedtableblock_to_alignedtypedtableblock)


def backward(apps, schema):
    migrate(apps, alignedtypedtableblock_to_typedtableblock)


class Migration(migrations.Migration):

    dependencies = [
        ("standardpages", "0027_add_aligned_columns"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=backward),
    ]
