import pytest
from api.helpers import prepare_sales, so_body

pytestmark = pytest.mark.api


# Czy zamówienie z poprawnymi danymi zapisuje się w stanie DRAFT
# dla właściwego klienta, z odpowiednia ilością pozycji
def test_create_sales_order_returns_draft(api):
    sales, customer, item = prepare_sales(api)
    body = so_body(customer["id"], [(item["id"], "5", "25.00")])

    response = api.create_sales_order(body, headers=sales)
    assert response.status_code == 201
    data = response.json()
    assert data["partnerId"] == customer["id"]
    assert data["status"] == "DRAFT"
    assert len(data["lines"]) == 1


# Czy dane są prawidłowo walidowane przy tworzeniu zamówienia
@pytest.mark.parametrize(
    "qty, price, description",
    [
        ("-5", "25.00", "negative quantity"),
        ("0", "25.00", "zero quantity"),
        ("5", "-10.00", "negative unit price"),
    ],
)
def test_create_sales_order_invalid_lines(api, qty, price, description):
    sales, customer, item = prepare_sales(api)
    body = so_body(customer["id"], [(item["id"], qty, price)])

    response = api.create_sales_order(body, headers=sales)
    assert response.status_code in (400, 422), description
