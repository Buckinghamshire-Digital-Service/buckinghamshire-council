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


def validate_linkedin_domain(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    hostname = "www.linkedin.com"
    if netloc != hostname:
        raise ValidationError(
            f"{value} is not a LinkedIn URL. The domain part must be {hostname}"
        )
