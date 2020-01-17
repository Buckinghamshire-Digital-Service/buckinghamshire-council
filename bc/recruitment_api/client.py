from django.conf import settings

from zeep import Client
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.constants import TALENTLINK_API_WSDL
from bc.recruitment_api.transports import ZeepAPIKeyTransport


def get_client(wsdl=TALENTLINK_API_WSDL):
    return Client(
        wsdl,
        transport=ZeepAPIKeyTransport(
            cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
        ),
        wsse=UsernameToken(
            settings.TALENTLINK_API_USERNAME, settings.TALENTLINK_API_PASSWORD
        ),
    )
