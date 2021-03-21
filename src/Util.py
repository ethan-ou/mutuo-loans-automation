from typing import List, Dict, Any
import URL

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    from mypy_extensions import TypedDict  # <=3.7

def reduce_dict_list(dict_list: List[Dict[str, Any]], key: str) -> List[Any]:
    return [d[key] for d in dict_list]