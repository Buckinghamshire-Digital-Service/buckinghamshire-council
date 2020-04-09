from wagtail.images.tests.utils import get_test_image_file

import factory


class ImageFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Image {n}")
    file = factory.LazyAttribute(get_test_image_file)

    class Meta:
        model = "images.CustomImage"


# VC TODO: test import_image_from_url
# For CustomImage import_image_from_url()
def mock_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "https://test.url/test.png":
        return MockResponse(
            {
                "headers": {"Content-Type": "image/png"},
                "content": "incomprehensiblefilecontent",
            },
            200,
        )

    return MockResponse(None, 404)


def mock_import_image_from_url(
    title, url, filename, talentlink_image_id=None, collection_name="imported"
):
    new_image = ImageFactory()
    new_image.title = title
    new_image.talentlink_image_id = talentlink_image_id
    new_image.save()

    return new_image
