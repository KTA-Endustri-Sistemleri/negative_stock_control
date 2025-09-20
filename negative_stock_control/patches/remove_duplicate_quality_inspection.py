import frappe

def execute():
    # Stock Settings meta'sını al
    meta = frappe.get_meta("Stock Settings")

    # quality_inspection_settings_section alanlarını topla
    duplicates = [df.fieldname for df in meta.fields if df.fieldname == "quality_inspection_settings_section"]

    if len(duplicates) > 1:
        # DB'deki fazlalıkları sil
        docfields = frappe.get_all(
            "DocField",
            filters={
                "parent": "Stock Settings",
                "fieldname": "quality_inspection_settings_section"
            },
            pluck="name"
        )
        if len(docfields) > 1:
            for name in docfields[1:]:
                frappe.db.delete("DocField", {"name": name})
            frappe.db.commit()
            frappe.logger().info("✅ Removed duplicate quality_inspection_settings_section in Stock Settings")
