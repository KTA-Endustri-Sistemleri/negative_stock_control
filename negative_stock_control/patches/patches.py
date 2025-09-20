import frappe

def apply_patch(*args, **kwargs):
    try:
        import erpnext.stock.utils
        from negative_stock_control.allow_negative_stock_validation import validate_negative_stock
        erpnext.stock.utils.validate_negative_stock = validate_negative_stock
        frappe.logger("negative_stock").info("✅ Monkey patch applied: validate_negative_stock overridden")
    except ImportError:
        frappe.logger("negative_stock").warning("⚠️ ERPNext not available yet, patch skipped")
