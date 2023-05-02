import re


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def convert_markdown_links_to_html(text):
    # url_regex matches cases like [link text](www.example.com)
    # or [link text](https://www.example.com)
    url_regex = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    # loop over matches and replace with html link
    for match in url_regex.finditer(text):
        if match.group(1) and match.group(2):
            link = match.group(2)
            link_text = match.group(1)

            # Add protocol if missing
            if not link.startswith("http"):
                link = "https://" + link

            text = text.replace(
                match.group(0), '<a href="{}">{}</a>'.format(link, link_text)
            )

    return text
