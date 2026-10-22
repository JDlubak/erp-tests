import pytest
from api.helpers import adjustment_body, prepare_adjustment

pytestmark = pytest.mark.api


# Czy nadwyżka (dodatnia korekta) jest księgowana jako dokument POSTED
def test_positive_adjustment_is_posted(api):
    warehouse, item, location = prepare_adjustment(api)

    response = api.create_stock_adjustment(
        adjustment_body(item["id"], location, "10"), headers=warehouse)
    assert response.status_code == 201
    adjustment = response.json()
    assert adjustment["status"] == "POSTED"
    assert adjustment["adjustmentNumber"]
    assert adjustment["itemId"] == item["id"]
    assert adjustment["locationId"] == location
    assert float(adjustment["qtyDelta"]) == 10
    assert adjustment["journalEntryId"] is not None
    assert adjustment["movementGroupId"]

    stock = api.get_item_on_hand(item["id"], headers=warehouse).json()
    assert float(stock["onHandQty"]) == 10
    assert float(stock["totalValue"]) == 50


# Czy strata większa niż stan jest odrzucana i stan się nie zmienia
def test_loss_exceeding_on_hand_returns_422(api):
    warehouse, item, location = prepare_adjustment(api)
    api.create_stock_adjustment(
        adjustment_body(item["id"], location, "5"), headers=warehouse)

    response = api.create_stock_adjustment(
        adjustment_body(item["id"], location, "-5.000001", unit_cost=None),
        headers=warehouse)
    assert response.status_code == 422

    stock = api.get_item_on_hand(item["id"], headers=warehouse).json()
    assert float(stock["onHandQty"]) == 5
