from lxml import html
from typing import Dict, List, Any
import URL

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7

class ItemPayload(TypedDict, total=False):
    item[name]: str
    item[summary]: str
    item[department_id]: int
    item[weight]: str
    item[replacement_cost]: str
    item[off_campus]: int
    item[publicly_viewable]: int
    item[online_booking_available]: int
    item[unique_assets]: int
    item[maximum_loan_duration_multiplyer]: str
    item[maximum_loan_duration_interval]: str
    item[default_loan_duration_multiplyer]: str
    item[default_loan_duration_interval]: str
    item[information]: str
    item[special_conditions]: str
    commit: str
    utf8: str
    authenticity_token: str

class Item(TypedDict):
    id: int
    url: str
    name: str

def url() -> str:
    return f"{URL.base}{URL.admin}{URL.items}"

def new_url() -> str:
    return f"{url()}{URL.new}"

def base_url() -> str:
    return f"{URL.admin}{URL.items}/"

def page_url(page: int) -> str:
    return f"{url()}?page={page}"

def item_url(url: str) -> str:
    return f"{URL.base}{url}"

def get_tags(html_string: str, base_url: str) -> List[Any]:
    tags = html.fromstring(html_string).xpath(f"//a[starts-with(@href, '{base_url}')]")

    # If a digit is at the end of a link, most likely an item.
    return [tag for tag in tags if tag.get('href').replace(base_url(), '').isdigit()]

# Check for dict
def find_item(items: List[Dict[str, Any]], name: str):
    return next((item for item in items if item['name'] == name), None)

# Check for dict
def find_new_items(items: List[Dict[str, Any]], existing_items):
    return [item for item in items if not find_item(existing_items, item['name'])]

def create_payload(name="", summary="", department_id=16, weight="", replacement_cost="", 
off_campus=1, publicly_viewable=1, online_booking_available=1, unique_assets=1, 
maximum_loan_duration_multiplyer="3", maximum_loan_duration_interval="Days", 
default_loan_duration_multiplyer="3", default_loan_duration_interval="Days",
information="", special_conditions="", commit="Save", utf8: "✓", authenticity_token="") -> Dict[str, Any]:
    return TypedDict('ItemPayload', {
        'item[name]': name,
        'item[summary]': summary,
        'item[department_id]': department_id,
        'item[weight]': weight,
        'item[replacement_cost]': replacement_cost,
        'item[off_campus]': off_campus,
        'item[publicly_viewable]': publicly_viewable,
        'item[online_booking_available]': online_booking_available,
        'item[unique_assets]': unique_assets,
        'item[maximum_loan_duration_multiplyer]': default_loan_duration_multiplyer,
        'item[maximum_loan_duration_interval]': default_loan_duration_interval,
        'item[default_loan_duration_multiplyer]': default_loan_duration_multiplyer,
        'item[default_loan_duration_interval]': default_loan_duration_interval,
        'item[information]': information,
        'item[special_conditions]': special_conditions,
        'commit': commit,
        'utf8': utf8,
        'authenticity_token': authenticity_token,
    })

def create_item(id=-1, name="", url=""):
    return TypedDict('Item', {
        'id': id,
        'url': url,
        'name': name
    })

def create_items_from_tags(tags, base_url):
    return [create_item(
        id=int(tag.get('href').replace(base_url, ''),
        name=tag.text,
        url=tag.get('href'))) for tag in tags]