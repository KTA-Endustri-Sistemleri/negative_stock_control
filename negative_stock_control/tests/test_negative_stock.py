import frappe
import unittest
import random
from frappe.exceptions import ValidationError


def get_or_create_company():
    """Varsayılan Test Company yoksa oluşturur"""
    if not frappe.db.exists("Company", "Test Company"):
        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "Test Company",
            "abbr": "TC",
            "default_currency": "USD"
        })
        company.insert(ignore_permissions=True)
        frappe.db.commit()
    return "Test Company"


def get_or_create_item(item_code="TEST-ITEM"):
    item_group = frappe.db.exists("Item Group", "Products") or "All Item Groups"
    if not frappe.db.exists("Item", item_code):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_code,
            "is_stock_item": 1,
            "maintain_stock": 1,
            "stock_uom": "Nos",
            "item_group": item_group
        })
        item.insert(ignore_permissions=True)
    return frappe.get_doc("Item", item_code)


def get_or_create_warehouse(base_name="WH-TEST"):
    company = get_or_create_company()  # 🔑 garanti company
    wh_name = f"{base_name}-{random.randint(1000,9999)}"
    wh = frappe.get_doc({
        "doctype": "Warehouse",
        "warehouse_name": wh_name,
        "company": company
    })
    wh.insert(ignore_permissions=True)
    return wh


def restrict_warehouse(warehouse):
    ss = frappe.get_single("Stock Settings")
    frappe.db.set_value("Stock Settings", None, "allow_negative_stock", 1)
    frappe.db.commit()
    frappe.clear_cache(doctype="Stock Settings")

    restricted = frappe.get_doc({
        "doctype": "Restricted Negative Stock Warehouse",
        "warehouse": warehouse.name,
        "parent": ss.name,
        "parentfield": "restricted_negative_stock_warehouses",
        "parenttype": "Stock Settings"
    })
    restricted.insert(ignore_permissions=True)
    ss.reload()
    print(f"[restrict_warehouse] {warehouse.name} eklendi")


class TestNegativeStock(unittest.TestCase):
    def setUp(self):
        # Varsayılan Item Group ekle
        if not frappe.db.exists("Item Group", "All Item Groups"):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": "All Item Groups",
                "is_group": 1,
                "parent_item_group": ""
            }).insert(ignore_permissions=True)

        # Varsayılan UOM ekle
        if not frappe.db.exists("UOM", "Nos"):
            frappe.get_doc({
                "doctype": "UOM",
                "uom_name": "Nos"
            }).insert(ignore_permissions=True)

        # Restricted tabloyu temizle
        frappe.db.sql("DELETE FROM `tabRestricted Negative Stock Warehouse`")
        frappe.db.commit()

        frappe.db.set_value("Stock Settings", None, "allow_negative_stock", 1)
        frappe.db.commit()
        frappe.clear_cache(doctype="Stock Settings")
        print("[setUp] Varsayılan Item Group & UOM garanti altına alındı, tablo temizlendi, allow_negative_stock=1 yapıldı")

    def test_negative_stock_restricted_warehouse(self):
        """Restricted depoda negatif stok yasak olmalı"""
        item = get_or_create_item()
        wh = get_or_create_warehouse("Restricted-WH")
        restrict_warehouse(wh)

        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "items": [{
                "item_code": item.item_code,
                "s_warehouse": wh.name,
                "qty": 5,
                "uom": "Nos",
                "conversion_factor": 1,
                "allow_zero_valuation_rate": 1
            }]
        })
        print(f"[restricted_test] Deneme: item={item.item_code}, wh={wh.name}, qty=5")

        with self.assertRaises(ValidationError):
            se.insert()

    def test_negative_stock_allowed_other_warehouse(self):
        """Restricted olmayan depoda negatif stok serbest olmalı"""
        item = get_or_create_item()
        wh = get_or_create_warehouse("Allowed-WH")

        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "items": [{
                "item_code": item.item_code,
                "s_warehouse": wh.name,
                "qty": 5,
                "uom": "Nos",
                "conversion_factor": 1,
                "allow_zero_valuation_rate": 1
            }]
        })
        print(f"[allowed_test] Deneme: item={item.item_code}, wh={wh.name}, qty=5")

        try:
            se.insert()
            ok = True
        except ValidationError as e:
            print(f"[allowed_test] ValidationError fırladı: {e}")
            ok = False

        self.assertTrue(ok, "Restricted olmayan depoda ValidationError atıldı!")
