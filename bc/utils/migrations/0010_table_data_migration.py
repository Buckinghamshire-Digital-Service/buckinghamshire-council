"""This data migration covers tweaking the table data.
https://projects.torchbox.com/projects/buckinghamshire-council/tickets/99

Current state:
    - CaptionedTableBlock contains a wagtail.contrib.typed_table_block.TypedTableBlock

Before:
    - BaseStoryBlock.table = custom CaptionedTableBlock
    - NestedStoryBlock.table = wagtail.contrib.table_block.TableBlock

After:
    - BaseStoryBlock.plain_text_table = wagtail.contrib.table_block.TableBlock
    - BaseStoryBlock.table = custom CaptionedTableBlock

    - NestedStoryBlock.plain_text_table = wagtail.contrib.table_block.TableBlock
    - NestedStoryBlock.table = custom CaptionedTableBlock

Changes in this data migration:
    - BaseStoryBlock.plain_text_table new and not affected.
    - BaseStoryBlock.table not affected.

    - NestedStoryBlock.plain_text_table new and not affected.
    - NestedStoryBlock.table values needs to be moved to plain_text_table.
"""

import copy
import json
from itertools import chain

from django.core.serializers.json import DjangoJSONEncoder
from django.db import migrations

from wagtail.core.blocks import StreamValue


def rename_table_to_plaintexttable(block):
    """Rename a `table` into `plain_text_table`.

    Returns the new object and whether it was mapped/updated or not.
    """
    if block["type"] == "table":
        return (
            {
                "type": "plain_text_table",
                "value": block["value"],
            },
            True,
        )

    return block, False


def rename_plaintexttable_to_table(block):
    """Rename a `plain_text_table` into `table`.

    Returns the new object and whether it was mapped/updated or not.
    """
    if block["type"] == "plain_text_table":
        return (
            {
                "type": "table",
                "value": block["value"],
            },
            True,
        )

    return block, False


def get_content_streamblock(old_content_blocks, mapper):
    mapped = False
    new_content_blocks = []

    for content_block in old_content_blocks:
        new_content_block, block_mapped = mapper(content_block)
        new_content_blocks.append(new_content_block)
        mapped = mapped or block_mapped

    return new_content_blocks, mapped


def get_new_stream_data(old_stream_data, mapper):
    """A loop for converting the blocks inside the streamfield."""

    stream_data = []
    mapped = False

    for block in old_stream_data:
        if block["type"] == "accordion":
            accordion_item_blocks = block["value"]["items"]
            new_accordion_item_blocks = []

            for accordion_item_block in accordion_item_blocks:
                # For some reason, some pages have an old data structure
                # where accordions had an extra structblock layer.
                # Update it to the expected data structure.
                if accordion_item_block.get("type", None) == "item":
                    new_content_blocks, block_mapped = get_content_streamblock(
                        accordion_item_block["value"]["content"], mapper
                    )
                    new_accordion_item_block = {
                        "title": accordion_item_block["value"]["title"]
                    }
                else:
                    new_content_blocks, block_mapped = get_content_streamblock(
                        accordion_item_block["content"], mapper
                    )
                    new_accordion_item_block = copy.deepcopy(accordion_item_block)

                mapped = mapped or block_mapped
                new_accordion_item_block["content"] = new_content_blocks
                new_accordion_item_blocks.append(new_accordion_item_block)

            new_block = copy.deepcopy(block)
            new_block["value"]["items"] = new_accordion_item_blocks
            stream_data.append(new_block)
        else:
            stream_data.append(block)

    return stream_data, mapped


def handle_object(obj, attrs, mapper):
    """Retrieves the object or page's streamfield data and
    calls get_new_stream_data using the streamfield data.
    """

    should_save = False
    for attr in attrs:
        # Skip the attribute if the object/page doesn't have it.
        if not hasattr(obj, attr):
            continue

        old_stream_data = getattr(obj, attr).raw_data
        stream_data, mapped = get_new_stream_data(old_stream_data, mapper)

        if mapped:
            raw_text = json.dumps(stream_data, cls=DjangoJSONEncoder)
            stream_block = old_stream_data

            # Same as obj.attr = StreamValue(...)
            setattr(
                obj,
                attr,
                StreamValue(stream_block, [], is_lazy=True, raw_text=raw_text),
            )
            should_save = True

    if should_save:
        obj.save()


def handle_revision(revision, attrs, mapper):
    """Retrieves the revision's streamfield data and
    calls get_new_stream_data using the streamfield data.
    """
    revision_content = json.loads(revision.content_json)

    should_save = False
    for attr in attrs:
        # Skip the attribute if the page doesn't have it.
        if attr not in revision_content:
            continue

        mapped = False
        stream_data = None

        old_stream_data = json.loads(revision_content[attr])
        stream_data, mapped = get_new_stream_data(old_stream_data, mapper)

        if mapped:
            revision_content[attr] = json.dumps(stream_data)
            revision.content_json = json.dumps(revision_content)
            should_save = True

    if should_save:
        revision.save()


def migrate(apps, mapper):
    # Pages
    ApteanRespondCaseFormPage = apps.get_model("cases", "ApteanRespondCaseFormPage")
    BlogAboutPage = apps.get_model("blogs", "BlogAboutPage")
    BlogPostPage = apps.get_model("blogs", "BlogPostPage")
    EventPage = apps.get_model("events", "EventPage")
    InformationPage = apps.get_model("standardpages", "InformationPage")
    InlineIndex = apps.get_model("inlineindex", "InlineIndex")
    InlineIndexChild = apps.get_model("inlineindex", "InlineIndexChild")
    LocationPage = apps.get_model("location", "LocationPage")
    LongformChapterPage = apps.get_model("longform", "LongformChapterPage")
    LongformPage = apps.get_model("longform", "LongformPage")
    NewsPage = apps.get_model("news", "NewsPage")
    RecruitmentIndexPage = apps.get_model("recruitment", "RecruitmentIndexPage")

    page_attrs = ["body"]
    for page in chain(
        ApteanRespondCaseFormPage.objects.all(),
        BlogAboutPage.objects.all(),
        BlogPostPage.objects.all(),
        EventPage.objects.all(),
        InformationPage.objects.all(),
        InlineIndex.objects.all(),
        InlineIndexChild.objects.all(),
        LocationPage.objects.all(),
        LongformChapterPage.objects.all(),
        LongformPage.objects.all(),
        NewsPage.objects.all(),
        RecruitmentIndexPage.objects.all(),
    ):
        handle_object(page, page_attrs, mapper)

        for revision in page.revisions.all():
            handle_revision(revision, page_attrs, mapper)


def forward(apps, schema_editor):
    migrate(apps, rename_table_to_plaintexttable)


def backward(apps, schema_editor):
    migrate(apps, rename_plaintexttable_to_table)


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward, backward),
    ]

    dependencies = [
        ("blogs", "0012_storyblock_table_and_plaintexttable"),
        ("cases", "0019_storyblock_table_and_plaintexttable"),
        ("events", "0027_storyblock_table_and_plaintexttable"),
        ("inlineindex", "0029_storyblock_table_and_plaintexttable"),
        ("location", "0008_storyblock_table_and_plaintexttable"),
        ("longform", "0023_storyblock_table_and_plaintexttable"),
        ("news", "0027_storyblock_table_and_plaintexttable"),
        ("recruitment", "0053_storyblock_table_and_plaintexttable"),
        ("standardpages", "0033_storyblock_table_and_plaintexttable"),
        ("utils", "0009_systemmessagessettings_search_input_help_text"),
    ]
