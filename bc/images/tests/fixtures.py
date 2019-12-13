from wagtail.images.tests.utils import get_test_image_file

import factory


class ImageFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Image {n}")
    file = factory.LazyAttribute(get_test_image_file)

    class Meta:
        model = "images.CustomImage"
