from io import BytesIO
from mimetypes import guess_extension

from django.core.files.images import ImageFile
from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Collection

import requests


class CustomImage(AbstractImage):
    talentlink_image_id = models.TextField(blank=True, max_length=255)

    admin_form_fields = Image.admin_form_fields + ("talentlink_image_id",)


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["image", "filter_spec", "focal_point_key"]]


def import_image_from_url(
    title, url, filename, talentlink_image_id=None, collection_name="imported"
):
    # Get or create collection
    try:
        collection = Collection.objects.get(name=collection_name)
    except Collection.DoesNotExist:
        root_collection = Collection.get_first_root_node()
        collection = root_collection.add_child(name=collection_name)

    image_file_response = requests.get(url)
    if image_file_response.status_code == 200:
        file_extension = guess_extension(image_file_response.headers["Content-Type"])
        image_filename = filename + file_extension
        image_file = ImageFile(
            BytesIO(image_file_response.content), name=image_filename
        )
        new_image = CustomImage(
            title=title,
            file=image_file,
            talentlink_image_id=talentlink_image_id,
            collection=collection,
        )
        # new_image.collection = collection
        new_image.save()
        return new_image
