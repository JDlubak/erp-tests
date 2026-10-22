from datetime import date
import pytest
from api.helpers import po_body, prepare

pytestmark = pytest.mark.api


# Czy utworzone zamówienie ma status DRAFT, numer i poprawne dane linii
def test_create_po_single_line(api):
    warehouse, vendor, item = prepare(api)
    body = po_body(vendor["id"], [(item["id"], "10", "5.25")])

    response = api.create_purchase_order(body, headers=warehouse)
    assert response.status_code == 201
    po = response.json()
    assert po["status"] == "DRAFT"
    assert po["poNumber"]
    assert po["partnerId"] == vendor["id"]
    assert po["orderDate"] == date.today().isoformat()
    assert len(po["lines"]) == 1
    line = po["lines"][0]
    assert line["itemId"] == item["id"]
    assert float(line["qtyOrdered"]) == 10
    assert float(line["unitPrice"]) == 5.25
    assert float(line["qtyReceived"]) == 0


# Czy niepoprawne wartości w linii zamówienia są odrzucane
@pytest.mark.parametrize(
    "qty, price, description",
    [
        ("0", "1", "ilość równa 0"),
        ("-1", "1", "ilość ujemna"),
        ("1", "-0.01", "cena ujemna"),
    ],
)
def test_create_po_invalid_line_value_returns_400(api, qty, price,
                                                  description):
    warehouse, vendor, item = prepare(api)
    body = po_body(vendor["id"], [(item["id"], qty, price)])

    response = api.create_purchase_order(body, headers=warehouse)
    assert response.status_code == 400, description
