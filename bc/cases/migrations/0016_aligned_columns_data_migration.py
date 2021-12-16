import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import migrations
from django.utils.html import strip_tags

from wagtail.core.blocks.stream_block import StreamValue


def typedtableblock_to_alignedtypedtableblock(block):
    if not (block and block.get("value")):
        return {
            "type": "table",
            "value": {"caption": "", "table": {"columns": [], "rows": []},},
        }

    new_columns = []
    new_rows = []
    column_types = [column["type"] for column in block["value"]["table"]["columns"]]

    for row in block["value"]["table"]["rows"]:
        new_row_values = []
        for ind, row_value in enumerate(row["values"]):
            new_row_values.append({"type": column_types[ind], "value": row_value})
        new_rows.append(new_row_values)

    for column in block["value"]["table"]["columns"]:
        if column["type"] == "numeric":
            new_column_type = "right_aligned_column"
        else:
            new_column_type = "left_aligned_column"
        new_columns.append({"type": new_column_type, "heading": column["heading"]})

    return {
        "type": "table",
        "value": {
            "caption": block["value"]["caption"],
            "table": {"columns": new_columns, "rows": [{"values": new_rows}]},
        },
    }


def alignedtypedtableblock_to_typedtableblock(block):
    # this assumes that all cells of a single column will have same datatype,
    # and all columns have equals number of rows
    if not (block and block.get("value")):
        return {
            "type": "table",
            "value": {"caption": "", "table": {"columns": [], "rows": []},},
        }

    column_types = [
        row_value["type"]
        for row_value in block["value"]["table"]["rows"][0]["values"][0]
    ]

    new_columns = []
    new_rows = []

    for ind, column in enumerate(block["value"]["table"]["columns"]):
        new_columns.append({"type": column_types[ind], "heading": column["heading"]})

    for row in block["value"]["table"]["rows"][0]["values"]:
        new_row_values = []
        for row_value in row:
            new_row_values.append(row_value)
        new_rows.append({"values": new_row_values})

    return {
        "type": "table",
        "value": {
            "caption": block["value"]["caption"],
            "table": {"columns": new_columns, "rows": [{"values": new_rows}]},
        },
    }


def get_stream_data(old_stream_data, mapper):
    stream_data = []
    mapped = False

    for block in old_stream_data:
        if block["type"] == "table":
            contentblock = mapper(block)
            stream_data.append(contentblock)
            mapped = True

        else:
            stream_data.append(block)

    return stream_data, mapped


def handle_page(page, attrs, mapper):
    should_save = False
    for attr in attrs:
        old_stream_data = getattr(page, attr).raw_data
        stream_data, mapped = get_stream_data(old_stream_data, mapper)

        if mapped:
            raw_text = json.dumps(stream_data, cls=DjangoJSONEncoder)
            stream_block = old_stream_data

            # Same as page.attr = StreamValue(...)
            setattr(
                page,
                attr,
                StreamValue(stream_block, [], is_lazy=True, raw_text=raw_text),
            )
            should_save = True

    if should_save:
        page.save()


def handle_revision(revision, attrs, mapper):
    revision_content = json.loads(revision.content_json)

    should_save = False
    for attr in attrs:
        mapped = False
        stream_data = None

        if attr in revision_content:
            old_stream_data = json.loads(revision_content[attr])
            stream_data, mapped = get_stream_data(old_stream_data, mapper)

        if mapped:
            revision_content[attr] = json.dumps(stream_data)
            revision.content_json = json.dumps(revision_content)

    if should_save:
        revision.save()


def migrate(apps, mapper):
    ApteanRespondCaseFormPage = apps.get_model("cases", "ApteanRespondCaseFormPage")

    pages = ApteanRespondCaseFormPage.objects.all()
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
        ("cases", "0015_add_aligned_columns"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
