import factory

from bc.utils.models import SystemMessagesSettings


class SystemMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SystemMessagesSettings

    title_404 = "Test title"
    body_404 = "<p>Test body</p>"
    body_no_search_results = "<p>Test no search result found</p>"
