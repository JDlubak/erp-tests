import pytest
from api.helpers import create_confirmed_po, create_draft_po

pytestmark = pytest.mark.api


# Czy po potwierdzeniu zamówienie DRAFT dostaje status CONFIRMED
def test_confirm_draft_po_changes_status_to_confirmed(api):
    warehouse, po = create_draft_po(api)

    response = api.confirm_purchase_order(po["id"], headers=warehouse)
    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"
    assert response.json()["id"] == po["id"]


# Czy nie można potwierdzić zamówienia dwa razy
def test_confirm_already_confirmed_po_returns_409(api):
    warehouse, po = create_confirmed_po(api)

    response = api.confirm_purchase_order(po["id"], headers=warehouse)
    assert response.status_code == 409
    fetched = api.get_purchase_order(po["id"], headers=warehouse).json()
    assert fetched["status"] == "CONFIRMED"
