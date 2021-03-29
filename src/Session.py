import requests
import mimetypes
import time
from pathlib import Path
from typing import List, Dict, Any
import URL, Selector, Auth, Items, Barcodes, Asset

def new():
    return requests.Session()

def authenticate(username: str, password: str, session) -> None:
    response = session.get(URL.base)
    authenticity_token = Selector.auth_token(response.content)
    
    payload = Auth.create_payload(zid=username, password=password, authenticity_token=authenticity_token)
    session.post(Auth.url(), params=payload)

    print("Logging In...")

def get_items(session) -> List[Any]:
    print("Getting Items...")
    
    all_items = []
    page = 1
    while True:
        response = session.get(Items.page_url(page))
        tags = Items.get_tags(response.content, Items.base_url())
        items = Items.create_items_from_tags(tags, Items.base_url())
        
        if len(items) == 0:
            return all_items

        all_items.extend(items)
        time.sleep(0.5)
        page = page + 1

def get_assets(item: Dict[str, Any], session) -> List[Dict[str, Any]]:
    response = session.get(Items.item_url(item['url']))
    ids = Asset.get_ids(response.content)

    return [Asset.create_item(
        id=id,
        barcode=Asset.get_barcode(response.content, id),
        name=Asset.get_name(response.content, id, item['url']),
    ) for id in ids]

def add_item(item: Dict[str, Any], session) -> None:
    response = session.get(Items.new_url())
    authenticity_token = Selector.auth_token(response.content)

    payload = Items.create_payload(authenticity_token=authenticity_token)
    payload.update(item)

    assert payload != None, "No Items Found!"

    session.post(Items.url(), params=payload)

    print(f"Added Item: {payload['item[name]']}")

def add_items(items: List[Dict[str, Any]], session) -> None:
    for item in items:
        add_item(item, session)
        time.sleep(0.5)

def add_asset(item, asset: Dict[str, Any], session) -> None:
    response = session.get(Items.item_url(item['url']))
    authenticity_token = Selector.auth_token(response.content)

    payload = Asset.create_payload(id=item['id'], authenticity_token=authenticity_token)
    payload.update(asset)

    assert payload != None, "No Assets Found!"

    session.post(Asset.url(item['url']), params=payload)

    print(f"Adding Asset for {item['name']}. Barcode: {payload['asset[barcode]']}")

def add_assets(item, assets: List[Dict[str, Any]], session) -> None:
    for asset in assets:
        add_asset(item, asset, session)
        time.sleep(0.5)

def check_barcodes(barcodes: List[str], session) -> List[str]:
    response = session.get(Barcodes.url())
    existing = Barcodes.get_barcodes(response.content)
    return Barcodes.find_matches(barcodes, existing)

def get_image(url: str, session) -> Dict[str, Any]:
    response = session.get(url)
    return {
        'mimetype': response.headers['content-type'],
        'ext': mimetypes.guess_extension(response.headers['content-type']),
        'file': response.content,
        'name': Path(url).stem
    }

def get_barcode(barcode, session) -> Dict[str, Any]:
    return get_image(Barcodes.barcode_url(barcode), session)

def get_barcodes(barcodes, session) -> List[Dict[str, Any]]:
    all_barcodes = []

    for barcode in barcodes:
        all_barcodes.append(get_barcode(barcode, session))
        time.sleep(0.5)

    return all_barcodes