import re


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def convert_markdown_links_to_html(text):
    # url_regex matches cases like [link](www.example.com) or simply www.example.com which may
    # include an http:// or https://
    url_regex = re.compile(
        r"\[([^\]]+)\]\(([^)]+)\)|((?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+[^\s]+)"
    )
    # loop over matches and replace with html link
    for match in url_regex.finditer(text):
        link = link_text = None
        # if match is a markdown link, use the link text and url
        if match.group(1) and match.group(2):
            link = match.group(2)
            link_text = match.group(1)
        # if match is a bare link, use the link as the link text and url
        elif match.group(3):
            link = match.group(3)
            link_text = match.group(3)
        if link and link_text:
            if not link.startswith("http"):
                link = "http://" + link
            text = text.replace(
                match.group(0), '<a href="{}">{}</a>'.format(link, link_text)
            )
    return text
