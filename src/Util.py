from typing import List, Dict, Any
import URL
from pathlib import Path

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7

def write_image(path: str, data) -> None:
    with open(path, "wb") as file:
        file.write(data)

def create_image_path(name: str, extension: str, folder: str = "") -> str:
    if len(folder) != 0:
        return str(Path(folder).joinpath(name + extension))
    else:
        return name + extension