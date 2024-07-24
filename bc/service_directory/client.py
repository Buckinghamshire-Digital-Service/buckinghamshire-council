import logging
from typing import Literal, Mapping, Optional

import requests

logger = logging.getLogger(__name__)


class BaseOutpostClient:
    def get(self, /, path: str, *, params: Mapping[str, str], **kwargs) -> Mapping:
        raise NotImplementedError


class ClientError(Exception):
    pass


class RequestsClient(BaseOutpostClient):
    timeout: float
    base_url: str

    def __init__(self, *, base_url: str, timeout: float = 5):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "www.buckinghamshire.gov.uk website"

    def get(self, /, path: str, *, params: Mapping[str, str], **kwargs) -> Mapping:
        return self.call("GET", path, params=params, **kwargs)

    def call(
        self,
        /,
        method: Literal["GET"],
        path: str,
        *,
        params: Mapping[str, str],
        **kwargs,
    ) -> Mapping:
        kwargs.setdefault("timeout", self.timeout)
        url = self.construct_url(path)
        logger.info("Making %s HTTP call to: %s (%r)", method, url, params)
        try:
            response = self.session.request(method, url, params=params, **kwargs)
        except requests.RequestException as e:
            raise ClientError from e
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise ClientError from e
        try:
            return response.json()
        except requests.JSONDecodeError as e:
            raise ClientError from e

    def construct_url(self, /, path: str, *, base_url: Optional[str] = None) -> str:
        if base_url is None:
            base_url = self.base_url
        if base_url.endswith("/") and path.startswith("/"):
            base_url = base_url[:-1]
        return f"{base_url}{path}"
