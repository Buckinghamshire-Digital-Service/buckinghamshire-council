import re


def format_case_reference(caseref):
    caseref = caseref.strip()
    pcre = re.compile(r"^[A-Z]{3}\s-\s\d+\b")
    match = pcre.match(caseref)
    return match and match[0] or caseref
