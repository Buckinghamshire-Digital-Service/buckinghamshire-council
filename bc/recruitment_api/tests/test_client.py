import pathlib
from unittest.mock import MagicMock

from django.test import TestCase, override_settings

import responses
from lxml import etree

from bc.recruitment_api.client import get_client
from bc.recruitment_api.constants import TALENTLINK_API_WSDL
from bc.recruitment_api.transports import ZeepAPIKeyTransport

wsdl_file_path = pathlib.Path(__file__).parent / "wsdl.xml"


class ClientTestMixin:
    def get_client(self):
        wsdl_file_path = pathlib.Path(__file__).parent / "wsdl.xml"
        wsdl_file_url = f"file://{wsdl_file_path}"
        return get_client(wsdl=wsdl_file_url)


class ClientTest(TestCase, ClientTestMixin):
    @responses.activate
    def test_creating_normal_client_calls_url(self):
        with open(wsdl_file_path, "r") as f:
            xml = f.read()
        responses.add(
            responses.GET, TALENTLINK_API_WSDL, xml, status=200, content_type="text/xml"
        )
        get_client()
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_creating_our_client_does_not_call_url(self):
        self.get_client()
        self.assertEqual(len(responses.calls), 0)


class TransportTest(TestCase):
    def test_vanilla(self):
        transport = ZeepAPIKeyTransport()
        self.assertEqual(transport.api_key, None)

    def test_with_api_key(self):
        api_key = "foo"
        transport = ZeepAPIKeyTransport(api_key=api_key)
        self.assertEqual(transport.api_key, api_key)

    def test_vanilla_post(self):
        transport = ZeepAPIKeyTransport()
        transport.session.post = MagicMock()
        url = "https://www.example.com"
        transport.post(url, "", headers={})
        transport.session.post.assert_called_once_with(
            url, data="", headers={}, timeout=transport.operation_timeout
        )

    def test_post_with_api_key(self):
        api_key = "foo"
        transport = ZeepAPIKeyTransport(api_key=api_key)
        transport.session.post = MagicMock()
        url = "https://www.example.com"
        url_with_api_key = f"{url}?api_key={api_key}"
        transport.post(url, "", headers={})
        transport.session.post.assert_called_once_with(
            url_with_api_key, data="", headers={}, timeout=transport.operation_timeout
        )


@override_settings(
    TALENTLINK_API_KEY="spam_key",
    TALENTLINK_API_USERNAME="eggs_username:ham:FO",
    TALENTLINK_API_PASSWORD="sausage",
)
class AuthenticationTest(TestCase):
    def setUp(self):
        expected = """
        <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
            <soap-env:Header>
                <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                    <wsse:UsernameToken>
                        <wsse:Username>eggs_username:ham:FO</wsse:Username>
                        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">sausage</wsse:Password>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soap-env:Header>
            <soap-env:Body>
                <ns0:getAdvertisementsByPage xmlns:ns0="http://ws.mrted.com/">
                    <ns0:pageNumber>1</ns0:pageNumber>
                </ns0:getAdvertisementsByPage>
            </soap-env:Body>
        </soap-env:Envelope>
        """  # noqa
        self.expected = "".join([x.strip() for x in expected.splitlines()])

    def test_api_key(self):
        client = get_client()

        root = client.create_message(
            client.service, "getAdvertisementsByPage", pageNumber=1
        )
        self.assertEqual(
            etree.tostring(root),
            etree.tostring(etree.fromstring(self.expected.encode())),
        )

    def test_api_key_with_request(self):
        client = get_client()
        client.transport.post = MagicMock()
        try:
            client.service.getAdvertisementsByPage(1)
        except Exception:  # We expect this, it receives no response
            pass
        name, args, kwargs = client.transport.post.mock_calls[0]
        url, body, headers = args
        root = etree.fromstring(body)
        nsmap = {}
        for el in root.iter():
            nsmap.update(el.nsmap)

        self.assertEqual(
            etree.tostring(root),
            etree.tostring(etree.fromstring(self.expected.encode())),
        )


class ZeepCacheTest(TestCase):
    # TODO
    pass
