import frappe

def execute():
    # CI ortamında duplicate quality_inspection_settings_section varsa temizle
    duplicates = frappe.get_all(
        "DocField",
        filters={
            "parent": "Stock Settings",
            "fieldname": "quality_inspection_settings_section"
        },
        pluck="name"
    )
    if len(duplicates) > 1:
        # İlk kaydı bırak, diğerlerini sil
        for name in duplicates[1:]:
            frappe.db.delete("DocField", {"name": name})
        frappe.db.commit()
        frappe.logger().info("✅ Removed duplicate quality_inspection_settings_section in Stock Settings")