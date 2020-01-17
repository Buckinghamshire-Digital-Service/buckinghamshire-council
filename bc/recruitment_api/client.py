from django.conf import settings

from zeep import Client, Settings
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.constants import TALENTLINK_API_WSDL
from bc.recruitment_api.transports import ZeepAPIKeyTransport

zeep_settings = Settings(strict=False, xml_huge_tree=True)


def get_client(wsdl=TALENTLINK_API_WSDL):
    return Client(
        wsdl,
        settings=zeep_settings,
        transport=ZeepAPIKeyTransport(
            cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
        ),
        wsse=UsernameToken(
            settings.TALENTLINK_API_USERNAME, settings.TALENTLINK_API_PASSWORD
        ),
    )
