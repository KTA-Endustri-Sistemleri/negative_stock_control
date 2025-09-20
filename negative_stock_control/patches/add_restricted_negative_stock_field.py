import frappe

def execute():
    if not frappe.db.exists("DocType", "Restricted Negative Stock Warehouse"):
        return  # child doctype tanımlı değilse çık

    if not frappe.db.exists("Custom Field", "Stock Settings-restricted_negative_stock_warehouses"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Stock Settings",
            "fieldname": "restricted_negative_stock_warehouses",
            "fieldtype": "Table",
            "label": "Negatif stoğa izin verilmeyecek depolar",
            "options": "Restricted Negative Stock Warehouse",
            "insert_after": "allow_negative_stock"
        }).insert()
        frappe.db.commit()
        frappe.logger().info("✅ Custom Field eklendi: Stock Settings.restricted_negative_stock_warehouses")
