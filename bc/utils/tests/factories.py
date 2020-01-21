import factory

from bc.utils.email import NotifyEmailMessage


class NotifyEmailMessageFactory(factory.Factory):
    class Meta:
        model = NotifyEmailMessage

    subject = "Test Subject"
    body = "Test body content"
