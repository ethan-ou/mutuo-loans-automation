from lxml import html

def auth_token(html_string: str) -> str:
    return html.fromstring(html_string).xpath('//input[@name="authenticity_token"]/@value')[0]