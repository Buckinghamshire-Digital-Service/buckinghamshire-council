import factory
import wagtail_factories


class IndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = "standardpages.IndexPage"

    title = factory.Sequence(lambda n: f"Section Index {n}")


class InformationPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = "standardpages.InformationPage"

    title = factory.Sequence(lambda n: f"Information Index {n}")
