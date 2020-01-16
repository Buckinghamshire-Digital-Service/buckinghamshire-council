from django.conf import settings

from zeep import Client, Settings
from zeep.wsse import UsernameToken

from bc.recruitment_api.cache import ZeepDjangoBackendCache
from bc.recruitment_api.constants import TALENTLINK_API_WSDL
from bc.recruitment_api.transports import ZeepAPIKeyTransport

transport = ZeepAPIKeyTransport(
    cache=ZeepDjangoBackendCache(), api_key=settings.TALENTLINK_API_KEY
)

zeep_settings = Settings(strict=False, xml_huge_tree=True)


def get_client():
    return Client(
        TALENTLINK_API_WSDL,
        settings=zeep_settings,
        transport=transport,
        wsse=UsernameToken(
            settings.TALENTLINK_API_USERNAME, settings.TALENTLINK_API_PASSWORD
        ),
    )
