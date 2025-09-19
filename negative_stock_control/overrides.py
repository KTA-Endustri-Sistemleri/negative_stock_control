import frappe
from frappe import _
from frappe.utils import flt

logger = frappe.logger("negative_stock", allow_site=True, file_count=5)


def stock_entry_validate(doc, method=None):
    logger.info(f"[stock_entry_validate] Checking Stock Entry {doc.name}")

    # Global ayarı oku
    allow_negative = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")
    logger.info(f"Global allow_negative_stock={allow_negative}")

    if not allow_negative:
        logger.info("Global negative stock kapalı → core default kontrol çalışacak")
        return

    # Restricted depoları al
    restricted_whs = set(frappe.get_all(
        "Restricted Negative Stock Warehouse",
        fields=["warehouse"],
        pluck="warehouse"
    ))

    logger.info(f"Restricted warehouses={restricted_whs}")

    for item in doc.items:
        if not item.s_warehouse:
            continue

        if item.s_warehouse not in restricted_whs:
            logger.info(f"Item {item.item_code} in WH {item.s_warehouse} → restricted değil, izin verildi")
            continue

        actual_qty = frappe.db.get_value(
            "Bin",
            {"warehouse": item.s_warehouse, "item_code": item.item_code},
            "actual_qty"
        ) or 0

        logger.info(f"Restricted WH {item.s_warehouse}: actual_qty={actual_qty}, request_qty={item.qty}")

        if flt(actual_qty) < flt(item.qty):
            logger.error(f"Negative stock denied for item={item.item_code}, wh={item.s_warehouse}")
            frappe.throw(
                _("Negative stock not allowed for Item {0} in Warehouse {1}")
                .format(item.item_code, item.s_warehouse)
            )