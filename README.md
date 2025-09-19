# Negative Stock Control

This app adds **per-warehouse negative stock restrictions** on top of
ERPNext's global "Allow Negative Stock" setting.

-   If **Allow Negative Stock** = Off → no negative stock anywhere.\
-   If **Allow Negative Stock** = On → negative stock is allowed
    globally, **except** in warehouses listed in the new child table in
    **Stock Settings**.

## Installation

``` bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/KTA-Endustri-Sistemleri/negative_stock_control.git
bench --site sitename install-app negative_stock_control --skip-assets
bench --site sitename migrate
bench build
bench restart
```

## Usage

1.  Go to **Stock Settings**.\
2.  Enable **Allow Negative Stock**.\
3.  You will see a new child table: **Restricted Negative Stock
    Warehouses**.\
4.  Add warehouses here to disallow negative stock in those locations.
