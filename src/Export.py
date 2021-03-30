from pathlib import Path
from csv import writer
from typing import Dict, List, Any

def create_path(name: str, extension: str, folder: str = "") -> str:
    if folder != "":
        return str(Path(folder).joinpath(name + extension))
    else:
        return name + extension

def check_folder(folder: str) -> None:
    Path(folder).mkdir(parents=True, exist_ok=True)

class BarcodeExport():
    def __init__(self, field_names: List[str]=['name', 'barcode']) -> None:
        self.field_names = field_names
        self.items = []

    def add_item(self, name: str, barcode: str) -> None:
        self.items.append([name, barcode])

    def add_items(self, name: str, barcodes: List[str]) -> None:
        for barcode in barcodes:
            self.items.append([name, barcode])

    def create_csv(self, path: str) -> None:
        with Path(path).open(mode='w', newline='') as file:
            writer_object = writer(file)
            writer_object.writerow(self.field_names)
            
            for item in self.items:
                writer_object.writerow(item)
            
            file.close()