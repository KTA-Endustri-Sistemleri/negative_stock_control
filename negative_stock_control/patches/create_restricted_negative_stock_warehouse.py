import frappe

def execute():
    if frappe.db.table_exists("Restricted Negative Stock Warehouse"):
        frappe.logger().info("✅ Restricted Negative Stock Warehouse tablosu zaten var, atlandı")
        return

    # Çocuk doctype tanımı
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Restricted Negative Stock Warehouse",
        "module": "Negative Stock Control",
        "istable": 1,
        "custom": 0,
        "fields": [
            {
                "fieldname": "warehouse",
                "fieldtype": "Link",
                "label": "Warehouse",
                "options": "Warehouse",
                "in_list_view": 1,
                "reqd": 1
            }
        ]
    })
    doctype.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.logger().info("✅ Restricted Negative Stock Warehouse tabloyu patch ile oluşturuldu")
