from django.conf import settings

from zeep import Client
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.transports import ZeepAPIKeyTransport


def get_client(wsdl=None, board=None):
    wsdl = wsdl or settings.TALENTLINK_API_WSDL
    if board == "internal":
        api_username = settings.TALENTLINK_INTERNAL_JOBS_API_USERNAME
    else:
        api_username = settings.TALENTLINK_API_USERNAME

    return Client(
        wsdl,
        transport=ZeepAPIKeyTransport(
            cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
        ),
        wsse=UsernameToken(api_username, settings.TALENTLINK_API_PASSWORD),
    )
