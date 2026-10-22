import pytest
from api.helpers import (
    auth_headers,
    create_customer,
    prepare_stocked_item,
    sales_invoice_body,
    shipment_body,
    so_body,
)

pytestmark = pytest.mark.api


# Czy można wystawić fakturę sprzedażową dla wydanego zamówienia sprzedaży
def test_create_sales_invoice_success(api):
    admin = auth_headers(api, "admin")
    sales = auth_headers(api, "sales")
    warehouse = auth_headers(api, "warehouse")
    accountant = auth_headers(api, "accountant")

    item_id, loc_id = prepare_stocked_item(api, qty="10")
    customer = create_customer(api, admin)

    so = api.create_sales_order(
        so_body(customer["id"], [(item_id, "2", "50.00")]),
        headers=sales).json()
    confirmed_so = api.confirm_sales_order(so["id"], headers=sales).json()
    so_line_id = confirmed_so["lines"][0]["id"]

    ship_res = api.create_shipment(
        shipment_body(so["id"], loc_id, [(so_line_id, "2")]),
        headers=warehouse)
    assert ship_res.status_code in (200, 201), ship_res.text

    invoice_res = api.create_sales_invoice(
        sales_invoice_body(so["id"], [(so_line_id, "2", "50.00")]),
        headers=accountant)
    assert invoice_res.status_code in (200, 201), invoice_res.text
    assert invoice_res.json()["salesOrderId"] == so["id"]
