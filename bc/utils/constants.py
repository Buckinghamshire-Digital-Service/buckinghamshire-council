RICH_TEXT_FEATURES = ["bold", "italic", "ol", "ul", "link", "document-link"]

RICH_PARAGRAPH_FEATURES = ["bold", "italic", "link", "document-link"]

BASE_PAGE_TEMPLATE = "patterns/base_page.html"
BASE_PAGE_TEMPLATE_FAMILY_INFORMATION = "patterns/base_page--fis.html"
BASE_PAGE_TEMPLATE_RECRUITMENT = "patterns/base_page--jobs.html"

ALERT_SUBSCRIPTION_STATUSES = {
    "STATUS_ALREADY_SUBSCRIBED": "already_subscribed",
    "STATUS_EMAIL_SENT": "email_sent",
    "STATUS_CONFIRMED": "confirmed",
    "STATUS_LINK_EXPIRED": "link_expired",
    "STATUS_UNSUBSCRIBED": "unsubscribed",
}

PLAIN_TEXT_TABLE_HELP_TEXT = """This table will be displayed as plain text on the page. You can add links to individuals cells by:
    <br>
    <ul>
        <li>simply pasting the link into the cell. e.g. if www.gov.uk is pasted onto the table, it will be
        output as <a href="http://www.gov.uk">www.gov.uk</a></li>
        <li>adding a link with a different link text, this can be done using the following syntax:
        [link text](www.gov.uk). This will output as <a href="http://www.gov.uk">link text</a></li>
    </ul>
    """
