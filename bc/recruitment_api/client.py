from django.conf import settings

from zeep import Client
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.transports import ZeepAPIKeyTransport


def get_client(wsdl=None, job_board=None):
    wsdl = wsdl or settings.TALENTLINK_API_WSDL

    # VC TODO: Concatenate setting name
    if job_board == "internal":
        api_username = settings.TALENTLINK_INTERNAL_JOBS_API_USERNAME
    elif job_board == "external":
        api_username = settings.TALENTLINK_API_USERNAME
    else:
        raise ValueError(f"No matching _JOBS_API_USERNAME job board '{job_board}'")

    return Client(
        wsdl,
        transport=ZeepAPIKeyTransport(
            cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
        ),
        wsse=UsernameToken(api_username, settings.TALENTLINK_API_PASSWORD),
    )
