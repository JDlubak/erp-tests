import re

import pytest
from playwright.sync_api import expect

from api.helpers import prepare_sales
from ui.pages.sales_page import SalesOrdersPage

pytestmark = pytest.mark.ui


# Czy stworzenie i potwierdzenie zamówienia formularzem poprawnie
# odzwierciedla stan w bazie
def test_sales_user_creates_and_confirms_sales_order(page, api,
                                                     sign_in_as):
    sales, customer, item = prepare_sales(api)
    sign_in_as("sales")
    orders = SalesOrdersPage(page).open()

    orders.create_order(customer["code"], item["sku"], "5", "20.00")

    toast = orders.notification(
        re.compile(r"Sales order SO-\d+ created"))
    expect(toast).to_be_visible()
    so_number = re.search(r"SO-\d+", toast.inner_text()).group(0)
    drawer = orders.drawer(so_number)
    expect(drawer.get_by_text("Draft", exact=True)).to_be_visible()

    orders.confirm_order(so_number)

    expect(orders.notification("Sales order confirmed")).to_be_visible()
    expect(drawer.get_by_text("Confirmed", exact=True)).to_be_visible()
    listed = api.get_sales_orders(headers=sales).json()
    created = next(so for so in listed if so["soNumber"] == so_number)
    assert created["partnerId"] == customer["id"]
    assert created["status"] == "CONFIRMED"


# Czy formularz zamówienia sprzedaży blokuje wysłanie z ujemną ilością
def test_sales_order_validation_rejects_invalid_qty(
        page, api, sign_in_as):
    sales, customer, item = prepare_sales(api)
    sign_in_as("sales")
    orders = SalesOrdersPage(page).open()

    orders.create_order(customer["code"], item["sku"], "-5", "20.00")

    expect(orders.dialog("New sales order")).to_be_visible()
    expect(orders.notification("created")).to_have_count(0)
