import pytest
from api.helpers import (auth_headers, create_customer,
                         create_draft_so, prepare_stocked_item,
                         shipment_body, so_body, stock_location_id)

pytestmark = pytest.mark.api


# Czy można zarejestrować wydanie towaru dla potwierdzonego
# zamówienia sprzedaży
def test_create_shipment_for_confirmed_sales_order(api):
    admin = auth_headers(api, "admin")
    sales = auth_headers(api, "sales")
    warehouse = auth_headers(api, "warehouse")

    item_id, loc_id = prepare_stocked_item(api, qty="10")
    customer = create_customer(api, admin)

    so = api.create_sales_order(
        so_body(customer["id"], [(item_id, "4", "30.00")]),
        headers=sales).json()
    confirmed_so = api.confirm_sales_order(so["id"],
                                           headers=sales).json()
    so_line_id = confirmed_so["lines"][0]["id"]

    response = api.create_shipment(
        shipment_body(so["id"], loc_id, [(so_line_id, "4")]),
        headers=warehouse)
    assert response.status_code in (200, 201)


# Czy wydanie towaru dla niepotwierdzonego zamówienia zwraca błąd
def test_create_shipment_for_draft_sales_order_fails(api):
    warehouse = auth_headers(api, "warehouse")
    _, draft_so = create_draft_so(api)
    loc_id = stock_location_id(api, warehouse)
    so_line_id = draft_so["lines"][0]["id"]

    response = api.create_shipment(
        shipment_body(draft_so["id"], loc_id, [(so_line_id, "5")]),
        headers=warehouse)
    assert response.status_code in (400, 409, 422)

