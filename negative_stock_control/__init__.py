def override_validate_negative_stock():
    import erpnext.stock.utils
    from negative_stock_control.allow_negative_stock_validation import validate_negative_stock
    erpnext.stock.utils.validate_negative_stock = validate_negative_stock

    import frappe
    frappe.logger("negative_stock").info("Monkey patch applied: erpnext.stock.utils.validate_negative_stock overridden")


# App yüklendiğinde patch uygula
override_validate_negative_stock()