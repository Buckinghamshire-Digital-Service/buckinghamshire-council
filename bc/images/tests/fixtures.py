from wagtail.images.tests.utils import get_test_image_file

import factory


class ImageFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Image {n}")
    file = factory.LazyAttribute(get_test_image_file)

    class Meta:
        model = "images.CustomImage"


def import_image_from_url_mock(
    title, url, filename, talentlink_image_id=None, collection_name="imported"
):
    import pdb

    pdb.set_trace()
    new_image = ImageFactory()
    new_image.title = title
    new_image.talentlink_image_id = talentlink_image_id
    new_image.save()

    return new_image
