from typing import List, Dict, Any
import csv

def read_csv(file_name: str) -> List[Dict[str, Any]]:
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        return [dict(row) for row in csv_reader]
