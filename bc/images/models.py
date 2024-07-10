import logging
import warnings
from io import BytesIO
from mimetypes import guess_extension

from django.core.files.images import ImageFile
from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Collection

import requests
from PIL.Image import DecompressionBombError, DecompressionBombWarning

logger = logging.getLogger(__name__)


class CustomImage(AbstractImage):
    talentlink_image_id = models.TextField(blank=True, max_length=255)

    admin_form_fields = Image.admin_form_fields + ("talentlink_image_id",)


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["image", "filter_spec", "focal_point_key"]]


class ImageImportException(Exception):
    pass


def get_validated_image_form(image_file, image_data):
    """Validate imported images as if uploaded through the Wagtail admin"""
    from wagtail.images.forms import get_image_form

    CustomImageForm = get_image_form(CustomImage)
    image_form = CustomImageForm(image_data, {"file": image_file})
    with warnings.catch_warnings():
        # Escalate DecompressionBombWarning to error level
        warnings.simplefilter("error", DecompressionBombWarning)
        try:
            if not image_form.is_valid():
                for field_name, errors in image_form.errors.items():
                    logger.warning(
                        f"Image validation failed in {field_name} importing {image_file.name} from TalentLink: {errors}"
                    )
        except (DecompressionBombError, DecompressionBombWarning) as e:
            logger.warning(
                f"Image validation failed importing {image_file.name} from TalentLink: {e}"
            )
            image_form.add_error("file", e)
    return image_form


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
        image_data = {
            "title": title,
            "talentlink_image_id": talentlink_image_id,
            "collection": collection,
        }

        image_form = get_validated_image_form(image_file, image_data)
        if image_form.errors:
            raise ImageImportException(
                f"File rejected due to validation errors:\n{image_form.errors.as_text()}"
            )

        new_image = image_form.save()
        return new_image
