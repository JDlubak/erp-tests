import pytest
from playwright.sync_api import expect

from api.helpers import create_draft_po
from ui.pages.purchasing_page import PurchaseOrdersPage

pytestmark = pytest.mark.ui


# Czy „Confirm order” w szufladzie zamówienia zmienia status
# Draft -> Confirmed w UI i w bazie
def test_confirm_draft_purchase_order(page, api, sign_in_as):
    warehouse, po = create_draft_po(api)
    number = po["poNumber"]
    sign_in_as("warehouse")
    orders = PurchaseOrdersPage(page).open()
    drawer = orders.open_order(number)
    expect(drawer.get_by_text("Draft", exact=True)).to_be_visible()

    orders.confirm_order(number)

    expect(orders.notification(
        "Purchase order confirmed")).to_be_visible()
    expect(drawer.get_by_text("Confirmed", exact=True)).to_be_visible()
    fetched = api.get_purchase_order(po["id"], headers=warehouse).json()
    assert fetched["status"] == "CONFIRMED"
