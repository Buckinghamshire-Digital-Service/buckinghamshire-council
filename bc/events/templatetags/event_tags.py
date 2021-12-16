from django import template

register = template.Library()


def format_date(date):
    date_str = ""
    if date is not None:
        date_str = f'{date.day} {date.strftime("%b")} {date.year}'
    return date_str


def format_time(time):
    time_str = ""
    if time is not None:
        if time.hour >= 12:
            if time.hour == 12:  # 12pm
                time_str += f"{12}"
            else:
                time_str += f"{time.hour - 12}"
            if time.minute:
                time_str += f" {time.minute}"
            time_str += "pm"
        else:
            if time.hour == 0:  # 12am
                time_str += f"{12}"
            else:
                time_str += f"{time.hour}"
            if time.minute:
                time_str += f" {time.minute}"
            time_str += "am"
    return time_str


@register.simple_tag
def format_event_date(start_date, start_time=None, end_date=None, end_time=None):
    start_date_str = format_date(start_date)
    start_time_str = format_time(start_time)
    end_date_str = format_date(end_date)
    end_time_str = format_time(end_time)
    if end_date and not end_date == start_date:
        return f"{start_date_str} {start_time_str} to {end_date_str} {end_time_str}"
    elif end_time:
        return f"{start_date_str} {start_time_str} to {end_time_str}"
    else:
        return f"{start_date_str} {start_time_str}"
