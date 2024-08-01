from django.core.files.base import ContentFile

import factory


class DocumentFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Document {n}")
    file = ContentFile("Test content")

    class Meta:
        model = "documents.CustomDocument"
