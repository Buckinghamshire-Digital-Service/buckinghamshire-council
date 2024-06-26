import factory

from bc.cases.backends.respond.constants import APTEAN_FORM_COMPLAINT


class ApteanRespondCaseFormPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cases.ApteanRespondCaseFormPage"

    title = factory.Sequence(lambda n: "Aptean Respond Case Form Page")
    listing_summary = "Aptean Respond Case Form Page"
    form = APTEAN_FORM_COMPLAINT
    completion_title = "foo"
