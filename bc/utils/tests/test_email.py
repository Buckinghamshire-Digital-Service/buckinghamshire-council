import uuid
from unittest import mock

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.test import TestCase, override_settings

from bc.utils.email import NotifyEmailBackend, NotifyEmailMessage
from bc.utils.tests.factories import NotifyEmailMessageFactory


class EmailMessageTest(TestCase):
    def test_basic(self):
        try:
            NotifyEmailMessage(subject="Test Subject", body="Test body content")
        except Exception:
            self.fail("Creating email message raised an exception unexpectedly.")

    def test_using_factory(self):
        try:
            NotifyEmailMessageFactory()
        except Exception:
            self.fail(
                "Creating email message from factory raised an exception unexpectedly."
            )

    def test_creating_with_one_recipient(self):
        try:
            NotifyEmailMessageFactory(to=["user@example.com"])
        except Exception:
            self.fail(
                "Creating email message with one recipient raised an exception unexpectedly."
            )

    def test_creating_with_multiple_recipients(self):
        try:
            NotifyEmailMessageFactory(
                to=["user@example.com", "another.user@example.com"]
            )
        except Exception:
            self.fail(
                "Creating email message with one recipient raised an exception unexpectedly."
            )

    def test_from_email_not_permitted(self):
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(from_email="webmaster@example.com")

    def test_attachments_not_permitted(self):
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(attachments=[("foo.txt", "Foo", "text/plain")])

    def test_custom_headers_not_permitted(self):
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(headers={"foo": "bar"})

    def test_cc_not_permitted(self):
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(cc=["webmaster@example.com"])

    def test_bcc_not_permitted(self):
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(bcc=["webmaster@example.com"])

    def test_attaching_not_permitted(self):
        email_message = NotifyEmailMessageFactory()
        with self.assertRaises(TypeError):
            email_message.attach("foo.txt", "Foo", "text/plain")

    def test_attaching_file_not_permitted(self):
        email_message = NotifyEmailMessageFactory()
        with self.assertRaises(TypeError):
            email_message.attach_file("foo.txt")

    def test_message_dict(self):
        message = NotifyEmailMessageFactory().message()
        self.assertIsInstance(message, dict)

    def test_default_subject_if_template_id_not_supplied(self):
        email_message = NotifyEmailMessageFactory()
        message = email_message.message()
        self.assertEqual(message["personalisation"]["subject"], email_message.subject)

    def test_default_body_if_template_id_not_supplied(self):
        email_message = NotifyEmailMessageFactory()
        message = email_message.message()
        self.assertEqual(message["personalisation"]["body"], email_message.body)

    def test_default_template_id_used_if_not_supplied(self):
        message = NotifyEmailMessageFactory().message()
        self.assertEqual(
            message["template_id"], settings.GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID
        )

    def test_custom_template_id(self):
        custom_template_id = str(uuid.uuid4())
        message = NotifyEmailMessageFactory(
            subject=None,
            body=None,
            template_id=custom_template_id,
            personalisation={"foo": "bar"},
        ).message()
        self.assertEqual(message["template_id"], custom_template_id)

    def test_bad_template_id(self):
        bad_template_id = "foo"
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(template_id=bad_template_id)

    def test_uuid_template_id(self):
        uuid_template_id = uuid.uuid4()
        with self.assertRaises(TypeError):
            NotifyEmailMessageFactory(template_id=uuid_template_id)

    def test_email_reply_to_id_is_used_if_not_supplied(self):
        message = NotifyEmailMessageFactory().message()
        self.assertNotIn("email_reply_to_id", message)

    def test_custom_email_reply_to_id(self):
        custom_email_reply_to_id = str(uuid.uuid4())
        message = NotifyEmailMessageFactory(
            email_reply_to_id=custom_email_reply_to_id
        ).message()
        self.assertEqual(message["email_reply_to_id"], custom_email_reply_to_id)

    def test_bad_email_reply_to_id(self):
        bad_email_reply_to_id = "foo"
        with self.assertRaises(ValueError):
            NotifyEmailMessageFactory(email_reply_to_id=bad_email_reply_to_id)

    def test_uuid_email_reply_to_id(self):
        uuid_email_reply_to_id = uuid.uuid4()
        with self.assertRaises(TypeError):
            NotifyEmailMessageFactory(email_reply_to_id=uuid_email_reply_to_id)


class EmailBackendConversionMethodTest(TestCase):
    def setUp(self):
        self.backend = NotifyEmailBackend(govuk_notify_api_key="not a real key")

    def test_convert_to_notify_message(self):
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
        )
        converted = self.backend.convert_to_notify_email_message(message)
        self.assertTrue(isinstance(converted, NotifyEmailMessage))

    def test_from_email_is_ignored(self):
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
        )
        self.assertEqual(message.from_email, "from@example.com")
        converted = self.backend.convert_to_notify_email_message(message)
        self.assertEqual(converted.from_email, None)

    def test_custom_headers_are_ignored(self):
        headers = {"Message-ID": "foo"}
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
            headers=headers,
        )
        self.assertEqual(message.extra_headers, headers)
        converted = self.backend.convert_to_notify_email_message(message)
        self.assertEqual(converted.extra_headers, {})

    def test_converting_with_attachments_not_permitted(self):
        attachments = [("foo.txt", "Foo", "text/plain")]
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
            reply_to=["another@example.com"],
            attachments=attachments,
        )
        self.assertEqual(message.attachments, attachments)
        with self.assertRaises(ValueError):
            self.backend.convert_to_notify_email_message(message)

    def test_converting_with_cc_addresses_not_permitted(self):
        cc = ["webmaster@example.com"]
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
            cc=cc,
        )
        self.assertEqual(message.cc, cc)
        with self.assertRaises(ValueError):
            self.backend.convert_to_notify_email_message(message)

    def test_converting_with_bcc_addresses_not_permitted(self):
        bcc = ["webmaster@example.com"]
        message = EmailMessage(
            "Hello",
            "Body goes here",
            "from@example.com",
            ["to1@example.com", "to2@example.com"],
            bcc=bcc,
        )
        self.assertEqual(message.bcc, bcc)
        with self.assertRaises(ValueError):
            self.backend.convert_to_notify_email_message(message)


@mock.patch("bc.utils.email.NotificationsAPIClient")
class EmailBackendTest(TestCase):
    def setUp(self):
        self.backend = NotifyEmailBackend(govuk_notify_api_key="not a real key")

    @override_settings(GOVUK_NOTIFY_API_KEY="fake settings key")
    def test_default_key(self, mock_client):
        backend = NotifyEmailBackend()
        self.assertEqual(backend.api_key, "fake settings key")
        message = NotifyEmailMessageFactory()
        backend.send_messages([message])
        mock_client.assert_has_calls([mock.call("fake settings key")])

    def test_creating_with_non_standard_key(self, mock_client):
        fake_key = "fake positional arg key"
        backend = NotifyEmailBackend(govuk_notify_api_key=fake_key)
        self.assertEqual(backend.api_key, fake_key)
        message = NotifyEmailMessageFactory()
        backend.send_messages([message])
        mock_client.assert_has_calls([mock.call(fake_key)])

    def test_we_can_send_notify_message_without_subject_or_body(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            template_id="43573f75-80e7-402f-b308-e5f1066fbd6f",
            personalisation={"foo": "bar"},
        )
        self.assertEqual(message.send(), 1)

    def test_we_can_send_notify_message_with_template_but_no_personalisation(
        self, mock_client
    ):
        """Test for using a template which does not have any variables"""
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            template_id="43573f75-80e7-402f-b308-e5f1066fbd6f",
        )
        self.assertEqual(message.send(), 1)

    def test_we_can_send_notify_message_with_only_subject_and_body(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"], subject="Subject", body="Message content"
        )
        self.assertEqual(message.send(), 1)

    def test_subject_without_body_is_not_allowed(self, mock_client):
        message = NotifyEmailMessage(to=["recipient@example.com"], subject="Subject")
        with self.assertRaises(ValueError):
            message.send()

    def test_body_without_subject_is_not_allowed(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"], body="Message content"
        )
        with self.assertRaises(ValueError):
            message.send()

    def test_subject_not_permitted_with_custom_template(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            subject="Subject",
            template_id="43573f75-80e7-402f-b308-e5f1066fbd6f",
            personalisation={"foo": "bar"},
        )
        with self.assertRaises(ValueError):
            message.send()

    def test_body_not_permitted_with_custom_template(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            body="Message content",
            template_id="43573f75-80e7-402f-b308-e5f1066fbd6f",
            personalisation={"foo": "bar"},
        )
        with self.assertRaises(ValueError):
            message.send()

    def test_personalisation_without_template_id_is_not_allowed(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"], personalisation={"foo": "bar"}
        )
        with self.assertRaises(ValueError):
            message.send()

    def test_template_id_not_permitted_with_subject_and_body(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            subject="Subject",
            body="Message content",
            template_id="43573f75-80e7-402f-b308-e5f1066fbd6f",
        )
        with self.assertRaises(ValueError):
            message.send()

    def test_personalisation_not_permitted_with_subject_and_body(self, mock_client):
        message = NotifyEmailMessage(
            to=["recipient@example.com"],
            subject="Subject",
            body="Message content",
            personalisation={"foo": "bar"},
        )
        with self.assertRaises(ValueError):
            message.send()


@mock.patch("bc.utils.email.NotificationsAPIClient")
@override_settings(
    EMAIL_BACKEND="bc.utils.email.NotifyEmailBackend",
    GOVUK_NOTIFY_API_KEY="not_a_real_key",
)
class DjangoInternalEmailAPITest(TestCase):
    """Tests of the django.core.send_mail function with the Notifications Backend"""

    def send_mail(self, **kwargs):
        options = {
            "subject": "Test Subject",
            "body": "Test body content",
            "from_email": "webmaster@example.com",
            "to": ["user@example.com"],
        }
        options.update(kwargs)
        return send_mail(
            options["subject"], options["body"], options["from_email"], options["to"]
        )

    def test_send_mail(self, mock_client):
        try:
            self.send_mail()
        except Exception:
            self.fail("django.core.mail.send_mail raised an exception unexpectedly")

    def test_send_mail_uses_notify_backend(self, mock_client):
        self.send_mail()
        mock_client().send_email_notification.assert_called_once()

    def test_send_mail_sends_to_correct_recipient(self, mock_client):
        recipients = ["recipient@example.com"]
        self.send_mail(to=recipients)
        mock_client().send_email_notification.assert_called_once()
        name, args, kwargs = mock_client().send_email_notification.mock_calls[0]
        self.assertEqual(kwargs["email_address"], recipients[0])

    def test_send_mail_to_multiple_recipients_results_in_multiple_calls(
        self, mock_client
    ):
        recipients = ["recipient1@example.com", "recipient2@example.com"]
        self.send_mail(to=recipients)
        mock_client().send_email_notification.assert_has_calls(
            [
                mock.call(
                    email_address="recipient1@example.com",
                    template_id=mock.ANY,
                    personalisation=mock.ANY,
                ),
                mock.call(
                    email_address="recipient2@example.com",
                    template_id=mock.ANY,
                    personalisation=mock.ANY,
                ),
            ]
        )

    def test_send_mail_comes_from_default_reply_to_address(self, mock_client):
        """Tests thath the email_reply_to_id kwarg is not supplied."""
        self.send_mail()
        mock_client().send_email_notification.assert_called_once()
        name, args, kwargs = mock_client().send_email_notification.mock_calls[0]
        self.assertNotIn("email_reply_to_id", kwargs)

    def test_send_mail_uses_plain_template(self, mock_client):
        subject = "This is the test subject"
        body = "This is the email content\nRegards\nTester"
        self.send_mail(subject=subject, body=body)
        mock_client().send_email_notification.assert_called_once_with(
            email_address=mock.ANY,
            template_id=settings.GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID,
            personalisation={"subject": subject, "body": body},
        )

    def test_send_mail_reports_number_sent(self, mock_client):
        self.assertEqual(self.send_mail(), 1)
        mock_client.reset_mock()
        self.assertEqual(self.send_mail(to=["a@example.com", "b@example.com"]), 1)
        # …even though two emails have been sent
        self.assertEqual(len(mock_client().send_email_notification.mock_calls), 2)
