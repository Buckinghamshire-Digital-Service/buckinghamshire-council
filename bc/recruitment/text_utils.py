import re
from functools import lru_cache


@lru_cache(maxsize=20)
def extract_salary_range(salary):
    double_salary_re = re.compile(
        r"(?P<first_salary>£[0-9,]+)(?P<above>\+?)[^£]*(?P<second_salary>£[0-9,]+)?"
    )
    match = double_salary_re.search(salary)
    if match:
        if match.group("first_salary") and match.group("second_salary"):
            return (
                re.sub(r"[£,]", "", match.group("first_salary")),
                re.sub(r"[£,]", "", match.group("second_salary")),
            )
        if match.group("first_salary") and match.group("above"):
            return (re.sub(r"[£,]", "", match.group("first_salary")), None)
        if match.group("first_salary"):
            return (None, re.sub(r"[£,]", "", match.group("first_salary")))
