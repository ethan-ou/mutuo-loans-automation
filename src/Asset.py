from lxml import html
from typing import List, Dict, Any
import URL, Util

def url(item_url) -> str:
    return f"{URL.base}{item_url}{URL.assets}"

def get_ids(html_string: str) -> List[int]:
    asset_base = 'asset_'
    ids = html.fromstring(html_string).xpath(f"//div[@id='assets']//tr[starts-with(@id, '{asset_base}')]/@id")
    return [int(asset.replace(asset_base, '')) for asset in ids]

# Gets barcode from assets table. This may change in the future.
def get_barcode(html_string: str, asset_id: int) -> str:
    return html.fromstring(html_string).xpath(f"//div[@id='assets']//tr[starts-with(@id, 'asset_{asset_id}')]//td[not(@class)]/text()")[0]

# Gets name from assets table. This may change in the future.
def get_name(html_string: str, asset_id: int, item_url: str) -> str:
    return html.fromstring(html_string).xpath(f"//div[@id='assets']//tr[starts-with(@id, 'asset_{asset_id}')]//td[not(@class)]//a[starts-with(@href, '{item_url}')]/text()")[0]

def create_payload(name="", make="", model="", serial_number="", barcode="",
off_campus=1, id=-1, authenticity_token="") -> Dict[str, Any]:
    return {
        'asset[name]': name,
        'asset[make]': make,
        'asset[model]': model,
        'asset[serial_number]': serial_number,
        'asset[barcode]': barcode,
        'asset[item_attributes][off_campus]': off_campus,
        'asset[item_attributes][id]': id,
        'utf8': "✓",
        'authenticity_token': authenticity_token,
    }

def create_item(id=-1, barcode="", name="") -> Dict[str, Any]:
    return {
        'id': id,
        'barcode': barcode,
        'name': name,
    }

def find_barcode_next(barcodes, stem) -> int:
    keys = [int(barcode.replace(stem, '')) for barcode in barcodes if stem in barcode]
    return 1 if len(keys) == 0 else sorted(keys)[-1] + 1

def find_name_next(names, stem) -> int:
    # Numbers are currently prefixed with a hash. Change if this is no longer the case.
    number_prefix = '#'

    keys = [int(name.replace(stem, '').strip().replace(number_prefix, '')) for name in names if stem in name]
    return 1 if len(keys) == 0 else sorted(keys)[-1] + 1