import Session, Reader, Parser, Items, Barcodes, Util, Export

required_keys = ["name", "summary", "replacement_cost", "quantity", "make", "model", "barcode_stem"]

def add_items_assets_from_csv(file: str, username: str, password: str, output_folder="barcodes"):
    csv_list = Reader.read_csv(file)
    Parser.check_csv(csv_list, required_keys)

    session = Session.new()
    response = Session.authenticate(username=username, password=password, session=session)

    # Add New Items
    current_items = Session.get_items(session)
    new_items = Items.find_new_items(csv_list, current_items)
    new_item_payloads = Parser.create_items(new_items)
    Session.add_items(new_item_payloads, session)
    
    # Add Assets
    current_items = Session.get_items(session)
    barcode_export = Export.BarcodeExport()
    for item in csv_list:
        selected = Items.find_item(name=item['name'], items=current_items)
        assets = Session.get_assets(selected, session)
        next_value = Parser.find_asset_next(item=item, assets=assets)
        
        asset_payloads = Parser.create_assets_from_quantity(item=item, barcode_value=next_value['barcode'], name_value=next_value['name'])

        # Check Barcodes
        Barcodes.warn_matches(Session.check_barcodes(barcodes=[asset['asset[barcode]'] for asset in asset_payloads], session=session))

        Session.add_assets(item=selected, assets=asset_payloads, session=session)

        # Barcode CSV Export
        barcode_export.add_items(item['name'], barcodes=[asset['asset[barcode]'] for asset in asset_payloads])
        
        # Custom Barcode Image Export
        # barcode_images = Session.get_barcodes(barcodes=[asset['asset[barcode]'] for asset in asset_payloads], session=session)
        # label_images = Util.create_barcode_labels_adapter(barcode_images, item['name'])
        # Util.create_images(label_images, "barcodes")
    
    Export.check_folder(output_folder)
    barcode_export.create_csv(path=Export.create_path(name="Barcodes", extension=".csv", folder="barcodes"))

def download_images_from_csv(file: str, output_folder="images"):
    session = Session.new()

    csv_list = Reader.read_csv(file)
    for item in csv_list:
        image = Session.get_image(url=item['image_url'], session=session, name=item['name'])
        Util.create_image(image_dict=image, folder=output_folder)