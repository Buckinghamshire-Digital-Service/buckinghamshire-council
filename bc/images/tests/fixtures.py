import factory


class ImageFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Image {n}")
    file = factory.django.ImageField()

    class Meta:
        model = "images.CustomImage"


def mock_import_image_from_url(
    title, url, filename, talentlink_image_id=None, collection_name="imported"
):
    new_image = ImageFactory()
    new_image.title = title
    new_image.talentlink_image_id = talentlink_image_id
    new_image.save()

    return new_image
