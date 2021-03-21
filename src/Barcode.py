from lxml import html
from typing import List
import URL

def url() -> str:
    return f"{URL.base}{URL.admin}{URL.items}{URL.barcodes}"

def barcode_url(barcode: str):
    return f"{URL.base}{URL.barcodes}/{barcode}"

def get_barcodes(html_string: str) -> List[str]:
    raw = html.fromstring(html_string).xpath("//div[@class='assets']//div[@class='asset']//div[@class='barcode']/text()")
    return list(filter(None, [barcode.replace('\n','').strip() for barcode in raw]))

def find_match(barcodes: List[str], existing_barcodes: List[str]):
    return set(barcodes).intersection(existing_barcodes)