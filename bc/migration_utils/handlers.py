import json

from django.core.serializers.json import DjangoJSONEncoder

from wagtail.blocks.stream_block import StreamValue


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
