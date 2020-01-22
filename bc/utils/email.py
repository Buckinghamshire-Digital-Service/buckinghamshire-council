import threading
import uuid
from typing import Optional

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, sanitize_address

from notifications_python_client.notifications import NotificationsAPIClient


class NotifyEmailMessage(EmailMessage):
    """An email message that knows how to work with GOV.UK Notify templates. """

    def __init__(
        self,
        subject="",
        body="",
        from_email=None,
        to=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        cc=None,
        reply_to=None,
        template_id: str = None,
        personalisation: Optional[dict] = None,
        email_reply_to_id: Optional[str] = None,
    ):
        if from_email:
            raise ValueError(
                "Custom from_email is not supported; use email_reply_to_id."
            )
        if attachments:
            raise ValueError("Attachments are not supported.")
        if headers:
            raise ValueError("Custom headers are not supported.")
        if cc:
            raise ValueError("CC recipients are not supported.")
        if bcc:
            raise ValueError("BCC recipients are not supported.")

        if template_id is not None:
            if not isinstance(template_id, str):
                raise TypeError("Template ID must be a UUID string.")
            try:
                uuid.UUID(template_id)
            except Exception as e:
                raise ValueError("Template ID must be a UUID string.") from e
        self.template_id = template_id

        self.personalisation = personalisation or {}

        if email_reply_to_id is not None:
            if not isinstance(email_reply_to_id, str):
                raise TypeError("email_reply_to_id must be a UUID string.")
            try:
                uuid.UUID(email_reply_to_id)
            except Exception as e:
                raise ValueError("email_reply_to_id must be a UUID string.") from e
        self.email_reply_to_id = email_reply_to_id

        super().__init__(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            bcc=bcc,
            connection=connection,
            attachments=attachments,
            headers=headers,
            cc=cc,
            reply_to=reply_to,
        )
        self.from_email = None

    def attach(self, *args, **kwargs):
        raise TypeError("Attachments are not supported by %s" % self.__class__.__name__)

    def attach_file(self, *args, **kwargs):
        raise TypeError("Attachments are not supported by %s" % self.__class__.__name__)

    def get_connection(self, fail_silently=False):
        """Only work with NotifyEmailBackend."""
        return NotifyEmailBackend(fail_silently=fail_silently)

    def validate_fields(self):
        if self.template_id is None:
            if not (self.subject and self.body):
                raise ValueError(
                    "If using the default template, subject and body are needed."
                )
            if self.personalisation:
                raise ValueError(
                    "If using the default template, do not supply a personalisation dict."
                )
        else:
            if self.subject or self.body:
                raise ValueError(
                    "Do not set subject or body with a custom template ID."
                )

    def message(self):
        self.validate_fields()
        if self.template_id is None:
            # Use the default plain template if one is not specified
            template_id = settings.GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID
            personalisation = {"subject": self.subject, "body": self.body}
        else:
            template_id = self.template_id
            personalisation = self.personalisation

        msg = {"template_id": template_id, "personalisation": personalisation}
        if self.email_reply_to_id:
            msg["email_reply_to_id"] = self.email_reply_to_id
        return msg


class NotifyEmailBackend(BaseEmailBackend):
    """A Django email backend that works with the GOV.UK Notify service."""

    def __init__(self, *args, **kwargs):
        self._lock = threading.RLock()
        self.client = None
        self.api_key = kwargs.get("govuk_notify_api_key", settings.GOVUK_NOTIFY_API_KEY)
        super().__init__(*args, **kwargs)

    def open(self):
        if self.client:
            return
        self.client = NotificationsAPIClient(self.api_key)

    def convert_to_notify_email_message(self, email_message):
        """Converts an EmailMessage instance to a NotifyEmailMessage.

        We silently ignore from_email, headers, and reply_to kwargs, because these are
        inserted by default by the django.core.send_mail function. Other attributes are
        passed on.
        """
        if not isinstance(email_message, NotifyEmailMessage):
            try:
                email_message = NotifyEmailMessage(
                    subject=email_message.subject,
                    body=email_message.body,
                    to=email_message.to,
                    bcc=email_message.bcc,
                    attachments=email_message.attachments,
                    cc=email_message.cc,
                )
            except Exception:
                if not self.fail_silently:
                    raise
        return email_message

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email messages
        sent.

        The GOV.UK Notify service requires one API request per recipient, and does not
        support CC or BCC addresses. Nonetheless the number returned by this method
        adheres to Django's default assumption of one email with multiple recipients
        equalling one "message" sent.
        """
        if not email_messages:
            return 0

        email_messages = [
            self.convert_to_notify_email_message(email_message)
            for email_message in email_messages
        ]

        if not email_messages:
            return 0

        with self._lock:
            self.open()
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False

        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        recipients = [
            sanitize_address(addr, encoding) for addr in email_message.recipients()
        ]
        message = email_message.message()
        try:
            for recipient in recipients:
                self.client.send_email_notification(email_address=recipient, **message)
        except Exception:
            if not self.fail_silently:
                raise
            return False
        return True
