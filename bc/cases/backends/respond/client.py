import hmac
import logging
from base64 import b64encode

from django.conf import settings
from django.core.cache import cache

import requests
from bs4 import BeautifulSoup

from .constants import (
    CATEGORY_INFO_TYPE,
    CREATE_CASE_SERVICES,
    CREATE_CASE_TYPE,
    FIELD_INFO_TYPE,
    RESPOND_CATEGORIES_CACHE_PREFIX,
    RESPOND_FIELDS_CACHE_PREFIX,
)
from .forms import CaseFormBuilder

logger = logging.getLogger(__name__)
client = None


class RespondClientException(Exception):
    pass


class RespondClient:
    """Wrapper for Aptean Respond API."""

    BASE_URL = settings.RESPOND_API_BASE_URL
    FORMS = "Forms"
    HMAC = "HMAC"
    authentication_method = FORMS

    def __init__(self):
        self.services = {CREATE_CASE_TYPE: {}}
        self.forms = {}
        self.field_mappings = {}

        # First catalogue the services we retrieve
        soup = self.get_web_service_meta_data()
        for webservice in soup.find_all("webservice"):
            name = webservice.find("name").text.strip()
            # url = webservice.urls.find("url").text
            # method = webservice.urls.find("url").attrs["method"]

            if webservice.attrs["type"] == CREATE_CASE_TYPE:
                if name not in CREATE_CASE_SERVICES:
                    logger.warning(
                        f"Unexpected CreateCase Web Service '{name}' encountered. It will be ignored."
                    )
                    continue

                self.services[CREATE_CASE_TYPE][name] = webservice

            if webservice.attrs["type"] == FIELD_INFO_TYPE:
                self.services[FIELD_INFO_TYPE] = name

            if webservice.attrs["type"] == CATEGORY_INFO_TYPE:
                self.services[CATEGORY_INFO_TYPE] = name

        self.cache_field_info()
        self.cache_category_info()

        # Generate form classes to replace the CaseCreate-type services
        for name, definition in self.services[CREATE_CASE_TYPE].items():
            self.services[CREATE_CASE_TYPE][name] = CaseFormBuilder(
                definition
            ).get_form_class()

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
        url = self.BASE_URL + path
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

    def get_fields(self, definition, **kwargs):
        return self.make_request(f"metadata.svc/Fields/{definition}", **kwargs)

    def get_categories(self, definition, **kwargs):
        return self.make_request(f"metadata.svc/Categories/{definition}", **kwargs)

    def create_case(self, definition, data, **kwargs):
        return self.make_request(
            f"case.svc/{definition}", method="post", data=data, raw=True, **kwargs
        )

    def cache_field_info(self):
        """Cache the field attributes."""
        """
        <field data-type="LongText" mandatory="true" read-only="false" schema-name="Case.Description" sid="64">
            <name base-locale="en-GB" base-value="Description"/>
            <description base-locale="en-GB" base-value=""/>
            <folder base-locale="en-GB" base-value="Case Details"/>
        </field>
        """
        service_name = self.services[FIELD_INFO_TYPE]
        soup = self.get_fields(service_name)
        for field in soup.find_all("field"):
            schema_name = field.attrs["schema-name"]
            options = {"required": field.attrs["mandatory"] == "true"}
            cache_key = RESPOND_FIELDS_CACHE_PREFIX + schema_name
            cache.set(cache_key, options)

    def cache_category_info(self):
        """Cache the choices for choice fields."""
        service_name = self.services[CATEGORY_INFO_TYPE]
        soup = self.get_categories(service_name)
        for field in soup.find_all("field"):
            schema_name = field.attrs["schema-name"]
            cache_key = RESPOND_CATEGORIES_CACHE_PREFIX + schema_name
            field_options = [
                o.find("name").text.strip()
                for o in field.find_all("option")
                if o.attrs["available"] == "true"
            ]
            choices = [(option, option) for option in field_options]
            cache.set(cache_key, choices)


def get_client():
    global client
    if client is None:
        client = RespondClient()
    return client
