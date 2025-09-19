import frappe
from frappe import _

def stock_entry_validate(doc, method=None):
    allow_negative = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    if not allow_negative:
        return

    restricted_whs = frappe.get_all(
        "Restricted Negative Stock Warehouse",
        fields=["warehouse"],
        pluck="warehouse"
    )
    restricted_whs = set(restricted_whs)

    for item in doc.items:
        # sadece çıkış depoları için kontrol
        if item.s_warehouse and item.s_warehouse in restricted_whs:
            actual_qty = frappe.db.get_value(
                "Bin",
                {"warehouse": item.s_warehouse, "item_code": item.item_code},
                "actual_qty"
            ) or 0
            if actual_qty < item.qty:
                frappe.throw(
                    _("Negative stock not allowed for Item {0} in Warehouse {1}")
                    .format(item.item_code, item.s_warehouse)
                )
