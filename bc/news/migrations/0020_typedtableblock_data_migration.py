import json

from django.db import migrations
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import strip_tags

from wagtail.core.blocks.stream_block import StreamValue


def tableblock_to_typedtableblock(block):
    has_table_header = block["value"]["first_row_is_table_header"]

    new_rows = []
    new_columns = []
    if len(block["value"]["data"]) > 0:
        for row_index, row in enumerate(block["value"]["data"]):
            current_row = []

            # If has table header, append to "columns" only.
            if row_index == 0:
                for col_index, cell in enumerate(row):
                    new_columns.append(
                        {
                            "heading": cell if has_table_header else "",
                            "type": "rich_text",
                        }
                    )

                if has_table_header:
                    continue

            # Append to "rows".
            for col_index, cell in enumerate(row):
                # If column header, set as bold.
                if block["value"]["first_col_is_header"] and col_index == 0:
                    current_row.append(f'<p class="row-header"><b>{cell}</b></p>')
                else:
                    current_row.append(f"<p>{cell}</p>")
            new_rows.append({"values": current_row})

    return {
        "type": "table",
        "value": {
            "caption": block["value"]["table_caption"],
            "table": {"columns": new_columns, "rows": new_rows},
        },
    }


def typedtableblock_to_tableblock(block):
    old_table = block["value"]["table"]

    new_data = []
    is_first_col_header = False

    # If any column headers is populated, add to data.
    header_data = [cell["heading"] for cell in old_table["columns"]]
    is_first_row_header = any(header_data)
    if is_first_row_header:
        new_data.append(header_data)

    # Populate data.
    for row in old_table["rows"]:
        current_row = []
        for cell in row["values"]:
            current_row.append(strip_tags(cell))
            # This assumes the block went through this data migration.
            # (Typed table blocks don't have column headers anyway.)
            if "row-header" in cell:
                is_first_col_header = True
        new_data.append(current_row)

    return {
        "type": "table",
        "value": {
            "cell": [],
            "data": new_data,
            "first_col_is_header": is_first_col_header,
            "first_row_is_table_header": is_first_row_header,
            "table_caption": block["value"]["caption"],
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
    NewsPage = apps.get_model("news", "NewsPage")

    pages = NewsPage.objects.all()
    for page in pages:
        handle_page(page, ["body"], mapper)

        for revision in page.revisions.all():
            handle_revision(revision, ["body"], mapper)


def forward(apps, schema):
    migrate(apps, tableblock_to_typedtableblock)


def backward(apps, schema):
    migrate(apps, typedtableblock_to_tableblock)


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0019_use_typedtableblock"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
