import pytest
from api.helpers import create_confirmed_po, create_draft_po, receive_goods

pytestmark = pytest.mark.api


# Czy pełne przyjęcie księguje GRN (POSTED), a zamówienie dostaje status
# RECEIVED
def test_full_receipt_posts_grn_and_marks_po_received(api):
    warehouse, po = create_confirmed_po(api)

    response = receive_goods(api, warehouse, po, "10")
    assert response.status_code == 201
    grn = response.json()
    assert grn["status"] == "POSTED"
    assert grn["grnNumber"]
    assert grn["purchaseOrderId"] == po["id"]
    line = grn["lines"][0]
    assert float(line["qtyReceived"]) == 10
    assert float(line["unitCost"]) == 5.00
    assert line["journalEntryId"] is not None
    assert line["movementGroupId"]

    fetched = api.get_purchase_order(po["id"], headers=warehouse).json()
    assert fetched["status"] == "RECEIVED"
    assert float(fetched["lines"][0]["qtyReceived"]) == 10


# Czy nie można przyjąć towaru do niepotwierdzonego zamówienia
def test_receipt_against_draft_po_returns_409(api):
    warehouse, po = create_draft_po(api)

    response = receive_goods(api, warehouse, po, "1")
    assert response.status_code == 409

    fetched = api.get_purchase_order(po["id"], headers=warehouse).json()
    assert fetched["status"] == "DRAFT"
    assert float(fetched["lines"][0]["qtyReceived"]) == 0
