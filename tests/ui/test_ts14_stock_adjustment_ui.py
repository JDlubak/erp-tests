import re

import pytest
from playwright.sync_api import expect

from api.helpers import auth_headers, create_item
from ui.pages.inventory_page import AdjustmentsPage

pytestmark = pytest.mark.ui


# Czy korekta stanu formularzem UI
# zwiększa rzeczywisty stan w bazie danych
def test_warehouse_posts_positive_stock_adjustment(page, api,
                                                   sign_in_as):
    admin = auth_headers(api, "admin")
    item = create_item(api, admin)
    sign_in_as("warehouse")
    adjustments = AdjustmentsPage(page).open()

    adjustments.post_adjustment(item["sku"], "10", "5.00",
                                "Inwentaryzacja UI")

    toast = adjustments.notification(
        re.compile(r"Adjustment ADJ-\d+ posted"))
    expect(toast).to_be_visible()
    expect(
        page.get_by_text(re.compile(r"Posted ADJ-\d+"))).to_be_visible()
    expect(page.get_by_text("qty 10")).to_be_visible()
    stock = api.get_item_on_hand(item["id"], headers=admin).json()
    assert float(stock["onHandQty"]) == 10
    assert float(stock["totalValue"]) == 50


# Czy próba korekty ujemnej przekraczającej stan magazynowy
# jest odrzucana
def test_warehouse_cannot_post_negative_adjustment_exceeding_stock(
        page,
        api,
        sign_in_as):
    admin = auth_headers(api, "admin")
    item = create_item(api, admin)
    sign_in_as("warehouse")
    adjustments = AdjustmentsPage(page).open()

    adjustments.post_adjustment(item["sku"], "-5", "5.00",
                                "Błędny odpis")

    expect(adjustments.notification(
        re.compile(r"Adjustment ADJ-\d+ posted"))).to_have_count(0)

    stock = api.get_item_on_hand(item["id"], headers=admin).json()
    assert float(stock["onHandQty"]) == 0
