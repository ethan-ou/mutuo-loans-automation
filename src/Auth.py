from lxml import html
from typing import List, Dict, Any
import URL

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7

class AuthPayload(TypedDict):
    zid: str
    password: str
    commit: str
    utf8: str
    authenticity_token: str

def url() -> str:
     return f"{URL.base}{URL.user_session}"

def create_payload(zid="", password="", commit="Login", utf8="✓", authenticity_token=""):
    return TypedDict('AuthPayload', {
        'user_session[zid]': zid, 
        'user_session[password]': password, 
        'commit': commit
        "authenticity_token": authenticity_token,
        "utf-8": utf8,
    })
