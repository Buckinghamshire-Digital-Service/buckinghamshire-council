import hmac
import logging
from base64 import b64encode

import requests
from bs4 import BeautifulSoup
from django.conf import settings

logger = logging.getLogger(__name__)
client = None


class RespondClientException(Exception):
    pass


class RespondClient:
    """Wrapper for Aptean Respond API."""

    FORMS = "Forms"
    HMAC = "HMAC"
    authentication_method = FORMS

    def __init__(self):
        self.WAGTAILADMIN_BASE_URL = settings.RESPOND_API_BASE_URL

    def get_respond_headers(self, url, data=""):
        db = settings.RESPOND_API_DATABASE
        username = settings.RESPOND_API_USERNAME
        password = settings.RESPOND_API_PASSWORD
        if self.authentication_method == self.FORMS:
            header = f'database="{db}",user="{username}",password="{password}"'
        else:
            msg = data or url
            hashed = hmac.new(
                key=b64encode(password.encode()), msg=b64encode(msg.encode())
            ).hexdigest()
            header = f'database="{db}",user="{username}",hash="{hashed}"'
        return {"RespondAuthentication": header}

    def make_request(self, path, method="get", data="", **kwargs):
        url = self.WAGTAILADMIN_BASE_URL + path
        headers = self.get_respond_headers(url)
        if data:
            headers["Content-Type"] = "application/xml"
        raw = kwargs.pop("raw", False)
        kwargs.update({"headers": headers})
        try:
            # if method == "post":
            #     import pdb; pdb.set_trace()
            response = requests.request(method, url, data=data, **kwargs)
        except requests.RequestException as e:
            logger.exception("Error communicating with Respond API")
            raise RespondClientException(str(e))
        if raw:
            return response
        soup = BeautifulSoup(response.content, "xml")
        return soup

    def get_web_service_meta_data(self, **kwargs):
        """The API documentation thinks metadata is two words."""
        return self.make_request("metadata.svc/getservices", **kwargs)

    def get_fields(self, **kwargs):
        definition = settings.RESPOND_GET_FIELDS_WEBSERVICE
        return self.make_request(f"metadata.svc/Fields/{definition}", **kwargs)

    def get_categories(self, **kwargs):
        definition = settings.RESPOND_GET_CATEGORIES_WEBSERVICE
        return self.make_request(f"metadata.svc/Categories/{definition}", **kwargs)

    def create_case(self, definition, data, **kwargs):
        return self.make_request(
            f"case.svc/{definition}", method="post", data=data, raw=True, **kwargs
        )


def get_client(force_refresh=False):
    global client
    if force_refresh or client is None:
        client = RespondClient()
    return client
