from django.conf import settings
from zeep import Client
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.transports import ZeepAPIKeyTransport


def get_client(wsdl=None, job_board=None):
    wsdl = wsdl or settings.TALENTLINK_API_WSDL

    # Each job_board should define on settings a corresponding API USERNAME
    # Eg. TALENTLINK_API_USERNAME_INTERNAL
    api_username = getattr(
        settings, "TALENTLINK_API_USERNAME_" + job_board.upper()
    )  # Will throw AttributeError if not defined.

    return Client(
        wsdl,
        transport=ZeepAPIKeyTransport(
            cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
        ),
        wsse=UsernameToken(api_username, settings.TALENTLINK_API_PASSWORD),
    )
