from django import template

register = template.Library()


def format_date(date):
    date_str = ""
    if date is not None:
        date_str = f'{date.day} {date.strftime("%b")} {date.year}'
    return date_str


def format_time(time):
    if not time:
        return ""
    if time.hour == 0 and time.minute == 0:
        return "midnight"
    if time.hour == 12 and time.minute == 0:
        return "midday"
    if time.minute:
        return time.strftime("%I:%M%p").lstrip("0").lower()
    return time.strftime("%I%p").lstrip("0").lower()


@register.simple_tag
def format_event_date(start_date, start_time=None, end_date=None, end_time=None):
    start_date_str = format_date(start_date)
    start_time_str = format_time(start_time)
    end_date_str = format_date(end_date)
    end_time_str = format_time(end_time)
    start_datetime_str = f"{start_date_str} {start_time_str}".strip(" ")
    end_datetime_str = f"{end_date_str} {end_time_str}".strip(" ")
    if end_date and not end_date == start_date:
        return f"{start_datetime_str} to {end_datetime_str}"
    elif end_time:
        return f"{start_datetime_str} to {end_time_str}".strip(" ")
    else:
        return start_datetime_str
