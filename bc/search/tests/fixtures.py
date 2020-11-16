import factory


class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "search.Term"
