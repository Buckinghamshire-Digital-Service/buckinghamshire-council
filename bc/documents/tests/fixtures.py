import factory
from django.core.files.base import ContentFile


class DocumentFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: f"Document {n}")
    file = ContentFile("Test content")

    class Meta:
        model = "documents.CustomDocument"
