from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_youtube_domain(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    hostnames = ["youtu.be", "www.youtube.com"]
    if netloc not in hostnames:
        raise ValidationError(
            (
                f'{value} is not a YouTube URL. The domain part must be one of {", ".join(hostnames)}'
            )
        )


def get_current_year():
    return now().year
