import factory


class IndexPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "standardpages.IndexPage"

    title = factory.Sequence(lambda n: f"Section Index {n}")


class InformationPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "standardpages.InformationPage"

    title = factory.Sequence(lambda n: f"Information Index {n}")
