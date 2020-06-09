import re


def get_case_reference(soup):
    try:
        return (
            soup.find("case")
            .find(attrs={"schemaName": "Case.FeedbackTypeReferenceNumber"})
            .get_text()
            .strip()
        )
    except AttributeError:
        return format_case_reference(soup.find("case").attrs["Name"])


def format_case_reference(caseref):
    caseref = caseref.strip()
    pcre = re.compile(r"^(?P<letters>[A-Z]{3})\s(-\s)?(?P<numbers>\d+\b)")
    match = pcre.match(caseref)
    return match and f"{match.group('letters')} {match.group('numbers')}" or caseref
