# Generated by Django 3.2.13 on 2023-03-07 09:34

from django.db import migrations


def sort_collections_order(apps, schema_editor):
    Collection = apps.get_model("wagtailcore.Collection")

    root_path = Collection.objects.get(depth=1).path
    root_child_collections = Collection.objects.filter(depth=2).order_by("name")

    alphabets = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapping = {}

    for i, collection in enumerate(root_child_collections, 1):
        new_colleciton_path = root_path + "000" + alphabets[i]
        mapping[collection] = new_colleciton_path
        descendants = Collection.objects.filter(path__startswith=collection.path)
        for descendant in descendants:
            mapping[descendant] = (
                new_colleciton_path + descendant.path.split(collection.path)[1]
            )

    for collection in root_child_collections:
        # give a randomized path to all collections, so that new paths can be assigned
        collection.path = "random-" + collection.path
        collection.save(update_fields=["path"])
    for collection, new_path in mapping.items():
        collection.path = new_path
        collection.save(update_fields=["path"])


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0011_wagtail_3_upgrade"),
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.RunPython(sort_collections_order, migrations.RunPython.noop),
    ]
