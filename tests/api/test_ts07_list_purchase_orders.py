import pytest
from api.helpers import auth_headers, create_draft_po

pytestmark = pytest.mark.api


# Czy lista zawiera świeżo utworzone zamówienie i czy można je pobrać po id
def test_list_and_get_po_details(api):
    warehouse, po = create_draft_po(api)

    list_res = api.get_purchase_orders(headers=warehouse)
    assert list_res.status_code == 200
    assert po["id"] in {order["id"] for order in list_res.json()}

    detail_res = api.get_purchase_order(po["id"], headers=warehouse)
    assert detail_res.status_code == 200
    fetched = detail_res.json()
    assert fetched["poNumber"] == po["poNumber"]
    assert fetched["status"] == "DRAFT"
    assert fetched["partnerId"] == po["partnerId"]
    assert fetched["lines"][0]["itemId"] == po["lines"][0]["itemId"]
    assert float(fetched["lines"][0]["qtyOrdered"]) == 10


# Czy nieistniejące zamówienie zwraca 404
def test_get_unknown_po_returns_404(api):
    warehouse = auth_headers(api, "warehouse")

    response = api.get_purchase_order(999999999, headers=warehouse)
    assert response.status_code == 404
