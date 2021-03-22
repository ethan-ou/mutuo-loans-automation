import Session, Reader, Parser

required_keys = ["name", "summary", "replacement_cost", "quantity", "make", "model", "barcode_stem"]

def check_valid(file: str):
    csv_list = Reader.read_csv(file)
    Parser.check_csv(csv_list, required_keys)

def add_items_assets_from_csv(file: str, username: str, password: str):
    csv_list = Reader.read_csv(file)
    Parser.check_csv(csv_list, required_keys)

    session = Session.new()
    Session.authenticate(username=username, password=password)