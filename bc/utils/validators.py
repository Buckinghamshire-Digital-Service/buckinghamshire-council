import os
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError


def validate_youtube_domain(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    hostnames = ["youtu.be", "www.youtube.com"]
    if netloc not in hostnames:
        raise ValidationError(
            (
                f'{value} is not a YouTube URL. The domain part must be one of {", ".join(hostnames)}'
            )
        )


class FileExtensionValidator:
    valid_extensions = []

    def __init__(self, valid_extensions=None):
        if valid_extensions is not None:
            if not isinstance(valid_extensions, list):
                raise TypeError("valid_extensions must be a list")
            self.valid_extensions = valid_extensions

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in self.valid_extensions:
            raise ValidationError(
                f"The attachment {value.name} has an unsupported file extension. "
                "You can upload files of the following types: "
                f"{', '.join(self.valid_extensions)}"
            )
