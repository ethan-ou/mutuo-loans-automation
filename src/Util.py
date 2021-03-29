from typing import List, Dict, Any
import URL
from pathlib import Path

def create_image(image_dict: Dict[str, Any], name="", folder="") -> None:
    final_name = name if name != "" else image_dict['name']

    path = create_image_path(name=final_name, extension=image_dict['ext'], folder=folder)
    if folder != "":
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    write_image(path=path, data=image_dict['file'])

    print(f"Image Created for {image_dict['name']}")

# TODO: Implement Names functionality
def create_images(image_dicts: List[Dict[str, Any]], folder="") -> None:
    for image_dict in image_dicts:
        create_image(image_dict=image_dict, folder=folder)

def write_image(path: str, data) -> None:
    with Path(path).open(mode="wb") as file:
        file.write(data)

def create_image_path(name: str, extension: str, folder: str = "") -> str:
    if folder != "":
        return str(Path(folder).joinpath(name + extension))
    else:
        return name + extension