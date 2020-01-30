from urllib.parse import urlsplit, urlunsplit

from zeep.transports import Transport


class ZeepAPIKeyTransport(Transport):
    def __init__(self, *args, api_key=None, **kwargs):
        self.api_key = api_key
        super().__init__(*args, **kwargs)

    def post(self, address, message, headers):
        if self.api_key:
            scheme, netloc, path, query, fragment = urlsplit(address)
            address = urlunsplit(
                (scheme, netloc, path, f"api_key={self.api_key}", fragment),
            )
        return super().post(address, message, headers)
