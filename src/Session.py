import requests
from typing import List, Any
import URL, Selector, Auth, Items, Barcode

def new():
    return requests.Session()

def authenticate(username: str, password: str, session) -> None:
    response = session.get(URL.base)
    authenticity_token = Selector.auth_token(response.content)
    
    payload = Auth.create_payload(zid=username, password=password, authenticity_token=authenticity_token)
    session.post(Auth.url(), params=payload)

    print("Logging In...")

def add_item(item, session) -> None:
    response = session.get(Items.new_url())
    authenticity_token = Selector.auth_token(response.content)

    payload = Items.create_payload(authenticity_token=authenticity_token).update(item)
    session.post(Items.url(), params=payload)

    print(f"Added Item: {payload['item[name]']}")

def add_items(items, session) -> None:
    for item in items:
        add_item(item, session)
        time.sleep(0.5)

def get_items(session) -> List[Any]:
    all_items = []
    page = 1
    while True:
        response = session.get(Items.page_url(page))
        tags = Items.get_tags(response.content, Items.base_url())
        items = Items.create_items_from_tags(tags, Items.base_url())
        
        if len(items) == 0:
            return all_items

        all_items.append(items)
        time.sleep(0.5)
        page = page + 1

def get_assets(item, session)

# TODO: Uploading images
