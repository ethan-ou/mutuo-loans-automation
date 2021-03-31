# ITEM KEYS:
# 'item[name]'
# 'item[summary]'
# 'item[department_id]'
# 'item[weight]'
# 'item[replacement_cost]'
# 'item[off_campus]'
# 'item[publicly_viewable]'
# 'item[online_booking_available]'
# 'item[unique_assets]'
# 'item[maximum_loan_duration_multiplyer]'
# 'item[maximum_loan_duration_interval]'
# 'item[default_loan_duration_multiplyer]'
# 'item[default_loan_duration_interval]'
# 'item[information]'
# 'item[special_conditions]'
# 'commit'
# 'utf8'
# 'authenticity_token'

# ASSET KEYS:
# 'asset[name]'
# 'asset[make]'
# 'asset[model]'
# 'asset[serial_number]'
# 'asset[barcode]'
# 'asset[item_attributes][off_campus]'
# 'asset[item_attributes][id]'
# 'utf8'
# 'authenticity_token'

settings = {
    'csv_keys': {
        "name": ["item:item[name]", "generate:asset:asset[name]:number"],
        "summary": "item:item[summary]",
        "replacement_cost": "item:item[replacement_cost]",
        "quantity": "special:asset:quantity",
        "make": "asset:asset[make]",
        "model": "asset:asset[model]",
        "barcode_stem": "special:asset:asset[barcode]:stem",
        "image_url": "special:image",
    }
}

