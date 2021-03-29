from lxml import html
from typing import List, Dict, Any
import URL

def url() -> str:
     return f"{URL.base}{URL.user_session}"

def create_payload(zid="", password="", commit="Login", utf8="✓", authenticity_token=""):
    return {
        'user_session[zid]': zid, 
        'user_session[password]': password, 
        'commit': commit,
        "authenticity_token": authenticity_token,
        "utf-8": utf8,
    }
