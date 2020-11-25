import re

from django.core.exceptions import ValidationError


def validate_postcode(postcode):
    """A UK postcode validator that also formats.

    A vanilla Django validator would return None for a valid value. Here we also return
    a nicely-formatted version of the postcode. This can be ignored if only form
    validation is needed.
    """
    postcode = postcode.strip()
    pcre = re.compile(
        r"^(?P<outward>[A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]?)(?P<space> ?)(?P<inward>[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$"  # noqa
    )
    match = pcre.match(postcode)
    if not match:
        raise ValidationError("Invalid Postcode")
    else:
        # The postcode matches a UK postcode regex. Format nicely.
        return f"{match.group('outward')} {match.group('inward')}".upper()


def area_from_district(district_name):
    """Strip a trailing " District Council" from a string."""
    return district_name.strip().split(" District Council")[0]


def clean_escaped_html(s):
    """
    Remove ASCII from HTML string.
    """
    htmlCodes = [
        "&#39;",
        "&quot;",
        "&gt;",
        "&lt;",
        "&amp;",
    ]
    for code in htmlCodes:
        s = s.replace(code, "")
    return s
