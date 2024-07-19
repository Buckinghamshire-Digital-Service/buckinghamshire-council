from collections.abc import Mapping
from typing import Literal

import requests


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

    def get(self, /, path: str, *, params: Mapping[str, str], **kwargs) -> Mapping:
        return self.call("GET", path, params=params, **kwargs)

    def call(self, /, method: Literal["GET"], path: str, **kwargs) -> Mapping:
        kwargs.setdefault("timeout", self.timeout)
        url = self.construct_url(path)
        try:
            response = self.session.request(method, url, **kwargs)
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

    def construct_url(self, /, path: str, *, base_url: str | None = None) -> str:
        if base_url is None:
            base_url = self.base_url
        return f"{base_url}{path}"
