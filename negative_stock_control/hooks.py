app_name = "negative_stock_control"
app_title = "negative_stock_control"
app_publisher = "Ufuk Karamalli"
app_description = "Per-warehouse negative stock control for ERPNext"
app_email = "ufukkaramalli@gmail.com"
app_license = "mit"

# Document Events
doc_events = {
    "Stock Entry": {
        "validate": "negative_stock_control.overrides.stock_entry_validate"
    }
}

# Run patch before fixtures are imported
before_app_install = "negative_stock_control.patches.remove_duplicate_quality_inspection.execute"

# Run patch again after migrations (safety net)
after_migrate = [
    "negative_stock_control.patches.remove_duplicate_quality_inspection.execute",
    "negative_stock_control.patches.patches.apply_patch",
]

# Overrides
override_whitelisted_methods = {
    "erpnext.stock.utils.validate_negative_stock":
        "negative_stock_control.allow_negative_stock_validation.validate_negative_stock"
}