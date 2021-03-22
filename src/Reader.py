import csv

def read_csv(file_name, csv_keys):
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        return [dict(row) for row in csv_reader]
