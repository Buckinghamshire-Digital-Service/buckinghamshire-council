import factory


class ApteanRespondCaseFormPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cases.ApteanRespondCaseFormPage"

    title = factory.Sequence(lambda n: f"Aptean Respond Case Form Page")
    web_service_definition = "TestCreateComplaints"
    completion_title = "foo"
