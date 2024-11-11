from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_facebook_domain(value):
    _, netloc, _, _, _ = urlsplit(value)
    hostnames = ["www.facebook.com", "facebook.com"]
    if netloc not in hostnames:
        raise ValidationError(
            f'{value} is not a Facebook URL. The domain part must be one of {", ".join(hostnames)}'
        )


def validate_youtube_domain(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    hostnames = ["youtu.be", "www.youtube.com"]
    if netloc not in hostnames:
        raise ValidationError(
            f'{value} is not a YouTube URL. The domain part must be one of {", ".join(hostnames)}'
        )


def validate_linkedin_domain(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    hostname = "www.linkedin.com"
    if netloc != hostname:
        raise ValidationError(
            f"{value} is not a LinkedIn URL. The domain part must be {hostname}"
        )


def get_current_year():
    return now().year
