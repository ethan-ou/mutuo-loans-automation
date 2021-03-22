from typing import List, Dict, Any
import Asset

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7

class CSVKeys(TypedDict):
    name: str
    summary: str
    replacement_cost: str
    quantity: str
    make: str
    model: str
    barcode_stem: str

# Matches subset of ItemPayload
class CSVItems(TypedDict):
    item[name]: str
    item[summary]: str
    item[replacement_cost]: str

# Matches subset of AssetPayload
class CSVAssets(TypedDict):
    asset[name]: str
    asset[make]: str
    asset[model]: str
    asset[barcode]: str

class NextAsset(TypedDict):
    barcode: str
    name: str

def check_csv(csv_list, required_keys) -> None:
    csv_keys = set.intersection(*tuple(set(line.keys()) for line in csv_list))
    missing_keys = csv_keys ^ set(required_keys)

    if missing_keys:
        raise Exception(f"CSV Keys Missing: {missing_keys}")

def create_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'item[name]': item['name'],
        'item[summary]': item['summary'],
        'item[replacement_cost]': item['replacement_cost']
    }

def create_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [create_item(item) for item in items]

def create_asset_from_quantity(item: Dict[str, Any], name_value: int, barcode_value: int) -> Dict[str, Any]:
    return {
        'asset[name]': f"{item['name']} #{name_value}",
        'asset[make]': item['make'],
        'asset[model]': item['model'],
        'asset[barcode]': f"{item['barcode_stem']}{barcode_value}",
    }

def create_assets_from_quantity(item: Dict[str, Any], name_value: int, barcode_value: int) -> List[Dict[str, Any]]:
    return [create_asset_from_quantity(item, name_value + i, barcode_value + i) for i in range(0, int(item['quantity']))]

def find_asset_next(item: Dict[str, Any], assets: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'barcode': Asset.find_barcode_next([asset['barcode'] for asset in assets], item['barcode_stem']),
        'name': Asset.find_name_next([asset['name'] for asset in assets], item['name'])
    }
