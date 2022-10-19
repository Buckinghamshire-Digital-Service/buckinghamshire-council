import factory


class NewsPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "news.NewsPage"

    title = factory.Sequence(lambda n: f"News Page {n}")
    listing_summary = "News Page"
