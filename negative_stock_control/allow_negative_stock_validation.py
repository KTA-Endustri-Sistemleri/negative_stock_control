import frappe
from frappe import _
from frappe.utils import flt

logger = frappe.logger("negative_stock", allow_site=True, file_count=5)


def validate_negative_stock(item_code, warehouse, qty, allow_negative_stock=None):
    logger.info(f"[validate_negative_stock] Start check: item={item_code}, wh={warehouse}, qty={qty}, allow={allow_negative_stock}")

    if not warehouse:
        logger.info("Warehouse boş → kontrol atlandı")
        return

    if allow_negative_stock is None:
        allow_negative_stock = frappe.db.get_single_value("Stock Settings", "allow_negative_stock")

    logger.info(f"Global allow_negative_stock={allow_negative_stock}")

    # Eğer globalde kapalıysa → core default hata
    if not allow_negative_stock:
        logger.warning(f"Global negative stock OFF → hata! item={item_code}, wh={warehouse}")
        _throw(item_code, warehouse)

    # Restricted depoları çek
    restricted_whs = set(frappe.get_all(
        "Restricted Negative Stock Warehouse",
        fields=["warehouse"],
        pluck="warehouse"
    ))

    logger.info(f"Restricted warehouses={restricted_whs}")

    # Eğer restricted değilse → kontrol etme
    if warehouse not in restricted_whs:
        logger.info(f"Warehouse {warehouse} restricted değil → izin verildi")
        return

    # Restricted depoda qty kontrolü
    actual_qty = frappe.db.get_value(
        "Bin",
        {"warehouse": warehouse, "item_code": item_code},
        "actual_qty"
    ) or 0

    logger.info(f"Warehouse {warehouse} actual_qty={actual_qty}, request_qty={qty}")

    if flt(actual_qty) < flt(qty):
        logger.error(f"Negative stock denied for item={item_code}, wh={warehouse}")
        _throw(item_code, warehouse)


def _throw(item_code, warehouse):
    frappe.throw(
        _("Negative stock not allowed for Item {0} in Warehouse {1}")
        .format(item_code, warehouse)
    )
