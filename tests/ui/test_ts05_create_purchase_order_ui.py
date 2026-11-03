import pytest
from playwright.sync_api import expect

from api.helpers import prepare
from ui.pages.purchasing_page import PurchaseOrdersPage

pytestmark = pytest.mark.ui


# Czy magazynier tworzy zamówienie zakupu formularzem, czy szuflada
# otwiera się w stanie Draft i czy zamówienie jest w bazie
def test_warehouse_creates_purchase_order(page, api, sign_in_as):
    warehouse, vendor, item = prepare(api)
    sign_in_as("warehouse")
    orders = PurchaseOrdersPage(page).open()

    orders.create_order(vendor["code"], item["sku"], "10", "5.00")

    po_number = orders.created_po_number()
    drawer = orders.drawer(po_number)
    expect(drawer).to_be_visible()
    expect(drawer.get_by_text("Draft", exact=True)).to_be_visible()
    listed = api.get_purchase_orders(headers=warehouse).json()
    created = next(po for po in listed if po["poNumber"] == po_number)
    assert created["partnerId"] == vendor["id"]
    assert created["status"] == "DRAFT"
