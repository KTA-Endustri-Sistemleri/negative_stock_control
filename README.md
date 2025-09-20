# Negative Stock Control

This application allows **restricting negative stock on selected warehouses** in **ERPNext v15.78.1**.  
Even if the global **Allow Negative Stock** setting is enabled, negative stock will be **denied** for chosen warehouses.

---

## 📌 Features
- **Global control**: If `Stock Settings > Stock Validations > Allow Negative Stock` is disabled → no warehouse allows negative stock.  
- **Warehouse-based restriction**: Even if global is enabled, warehouses listed in `Restricted Negative Stock Warehouse` are blocked.  
- **Flexibility**: Warehouses not listed remain unrestricted.  

---

## ⚙️ Installation

```bash
cd frappe-bench
bench get-app https://github.com/KTA-Endustri-Sistemleri/negative_stock_control.git
bench --site sitename install-app negative_stock_control
bench --site sitename migrate
```

---

## 🚀 Usage

1. Go to **Stock Settings** in ERPNext.  
2. Enable **Allow Negative Stock**.  
3. In the new table below, add warehouses where negative stock should be restricted.  
4. Now:  
   - Restricted warehouses → **ValidationError** if negative stock.  
   - Other warehouses → negative stock is allowed.  

---
[![ERPNext App Tests](https://github.com/KTA-Endustri-Sistemleri/negative_stock_control/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/KTA-Endustri-Sistemleri/negative_stock_control/actions/workflows/tests.yml)
## 🧪 Tests

Two scenarios are validated:  
1. Negative stock **restricted warehouse** → must raise error ✅  
2. Negative stock **non-restricted warehouse** → must pass ✅  

Run tests:  

```bash
bench --site sitename run-tests --app negative_stock_control
```

---

## 🔄 Continuous Integration

This repo includes **GitHub Actions** for automated testing.  
Tests run on **every push and pull request**.  

### 📂 Workflow

Defined in `.github/workflows/tests.yml`.  

### ✅ Benefits
- Automatic test on each commit  
- PRs require tests to pass before merge  
- Early bug detection  

---

## 📜 License
MIT
