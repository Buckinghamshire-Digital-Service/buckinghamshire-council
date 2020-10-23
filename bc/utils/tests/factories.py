import factory

from bc.utils.email import NotifyEmailMessage
from bc.utils.models import SystemMessagesSettings


class NotifyEmailMessageFactory(factory.Factory):
    class Meta:
        model = NotifyEmailMessage

    subject = "Test Subject"
    body = "Test body content"


class SystemMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SystemMessagesSettings

    title_404 = "Test title"
    body_404 = "<p>Test body</p>"
    body_no_search_results = "<p>Test no search result found</p>"
