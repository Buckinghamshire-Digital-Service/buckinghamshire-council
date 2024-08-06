import logging
from typing import Literal, Mapping, Optional, Type

import requests

logger = logging.getLogger(__name__)


class BaseServiceDirectoryClient:
    def __init__(self, *, base_url: str, timeout: Optional[float] = 5):
        raise NotImplementedError

    def get(
        self, /, path: str, *, params: Optional[Mapping[str, str]] = None, **kwargs
    ) -> Mapping:
        raise NotImplementedError


class ServiceDirectoryClientError(Exception):
    pass


class ServiceDirectoryRequestsClient(BaseServiceDirectoryClient):
    timeout: Optional[float]
    base_url: str

    def __init__(self, *, base_url: str, timeout: Optional[float] = 5):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "www.buckinghamshire.gov.uk website"

    def get(
        self, /, path: str, *, params: Optional[Mapping[str, str]] = None, **kwargs
    ) -> Mapping:
        return self.call("GET", path, params=params, **kwargs)

    def call(
        self,
        /,
        method: Literal["GET"],
        path: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        **kwargs,
    ) -> Mapping:
        kwargs.setdefault("timeout", self.timeout)
        url = self.construct_url(path)
        logger.info("Making %s HTTP call to: %s (%r)", method, url, params)
        try:
            response = self.session.request(method, url, params=params, **kwargs)
        except requests.RequestException as e:
            raise ServiceDirectoryClientError from e
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise ServiceDirectoryClientError from e
        try:
            return response.json()
        except requests.JSONDecodeError as e:
            raise ServiceDirectoryClientError from e

    def construct_url(self, /, path: str, *, base_url: Optional[str] = None) -> str:
        if base_url is None:
            base_url = self.base_url
        return "/".join((base_url.rstrip("/"), path.lstrip("/")))


def get_api_client_class() -> Type[BaseServiceDirectoryClient]:
    # TODO: Implement mock client for local dev and testing.
    return ServiceDirectoryRequestsClient
