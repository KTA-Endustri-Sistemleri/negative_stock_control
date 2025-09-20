import frappe

def execute():
    from negative_stock_control.patches import remove_duplicate_quality_inspection
    try:
        remove_duplicate_quality_inspection.execute()
    except Exception as e:
        frappe.log_error(f"Apply patch failed: {e}", "negative_stock_control.apply_patch")
