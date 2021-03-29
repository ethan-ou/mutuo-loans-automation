from lxml import html
from typing import Dict, List, Any
import URL

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
    return [tag for tag in tags if tag.get('href').replace(base_url, '').isdigit()]

# Check for dict
def find_item(name: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return next((item for item in items if item['name'] == name), None)

# Check for dict
def find_new_items(items: List[Dict[str, Any]], existing_items) -> List[Dict[str, Any]]:
    return [item for item in items if not find_item(item['name'], existing_items)]

def create_payload(name="", summary="", department_id=16, weight="", replacement_cost="", 
off_campus=1, publicly_viewable=1, online_booking_available=1, unique_assets=1, 
maximum_loan_duration_multiplyer="3", maximum_loan_duration_interval="Days", 
default_loan_duration_multiplyer="3", default_loan_duration_interval="Days",
information="", special_conditions="", commit="Save", authenticity_token="") -> Dict[str, Any]:
    return {
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
        'utf8': "✓",
        'authenticity_token': authenticity_token,
    }

def create_item(id=-1, name="", url=""):
    return {
        'id': id,
        'url': url,
        'name': name
    }

def create_items_from_tags(tags, base_url):
    return [create_item(
        id=int(tag.get('href').replace(base_url, '')),
        name=tag.text,
        url=tag.get('href')
    ) for tag in tags]