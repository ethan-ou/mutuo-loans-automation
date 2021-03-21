import csv

csv_keys = ["name", "summary", "replacement_cost", "quantity", "make", "model", "barcode_stem"]

def csv(file_name, csv_keys):
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        missing_keys = set(csv_reader.fieldnames) ^ set(csv_keys)
        if missing_keys:
            raise Exception(f"CSV Keys Missing: {missing_keys}")
        
        return [dict(row) for row in csv_reader]
