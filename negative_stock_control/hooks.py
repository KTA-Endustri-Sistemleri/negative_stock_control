from . import __version__ as app_version

app_name = "negative_stock_control"
app_title = "Negative Stock Control"
app_publisher = "Ufuk Karamalli"
app_description = "Per-warehouse negative stock control for ERPNext"
app_email = "ufukkaramalli@gmail.com"
app_license = "mit"

doc_events = {
    "Stock Entry": {
        "validate": "negative_stock_control.overrides.stock_entry_validate"
    }
}

override_whitelisted_methods = {
    "erpnext.stock.utils.validate_negative_stock": 
        "negative_stock_control.allow_negative_stock_validation.validate_negative_stock"
}

before_app_install = [
    "negative_stock_control.patches.remove_duplicate_quality_inspection.execute"
]

before_migrate = [
    "negative_stock_control/negative_stock_control/patches/create_restricted_negative_stock_warehouse.py",
    "negative_stock_control.patches.remove_duplicate_quality_inspection.execute"

]

after_migrate = [
    "negative_stock_control.patches.apply_patch.apply_patch"
]