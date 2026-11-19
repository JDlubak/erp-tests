from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import (auth_headers, create_customer, prepare_stocked_item,
                         sales_invoice_body, shipment_body, so_body)

# BDD-05 (TS-21, z krokami z TS-09, TS-10, TS-12): pełny przebieg zamówienia
# sprzedaży; powiela API-18 (test_ts09), API-20 (test_ts10), API-24 (test_ts12)
# i API-41 (test_ts21)
scenarios("features/ts21_sales_order_to_invoice.feature")


@given(parsers.parse(
    "a new customer and a sales item with {qty:d} units in stock"))
def customer_and_stocked_sales_item(api, ctx, qty):
    admin = auth_headers(api, "admin")
    ctx["item_id"], ctx["loc_id"] = prepare_stocked_item(api, qty=str(qty))
    ctx["customer"] = create_customer(api, admin)


@when(parsers.parse(
    "I create a sales order for {qty:d} units at {price} each"))
def create_sales_order(api, ctx, qty, price):
    body = so_body(ctx["customer"]["id"], [(ctx["item_id"], str(qty), price)])
    ctx["response"] = api.create_sales_order(body, headers=ctx["headers"])


@then(parsers.parse(
    "the sales order should be saved as a draft for the customer "
    "with {lines:d} line"))
def sales_order_saved_as_draft(ctx, lines):
    response = ctx["response"]
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["partnerId"] == ctx["customer"]["id"]
    assert data["status"] == "DRAFT"
    assert len(data["lines"]) == lines
    ctx["so"] = data


@when("I confirm the sales order")
def confirm_sales_order(api, ctx):
    ctx["response"] = api.confirm_sales_order(ctx["so"]["id"],
                                              headers=ctx["headers"])


@then("the sales order should be confirmed")
def sales_order_confirmed(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "CONFIRMED"
    ctx["so_line_id"] = response.json()["lines"][0]["id"]


@when(parsers.parse("I ship {qty:d} units of the sales order from stock"))
def ship_sales_order(api, ctx, qty):
    body = shipment_body(ctx["so"]["id"], ctx["loc_id"],
                         [(ctx["so_line_id"], str(qty))])
    ctx["response"] = api.create_shipment(body, headers=ctx["headers"])


@then("the shipment should be registered")
def shipment_registered(ctx):
    response = ctx["response"]
    assert response.status_code in (200, 201), response.text


@when(parsers.parse(
    "I invoice {qty:d} units of the sales order at {price} each"))
def invoice_sales_order(api, ctx, qty, price):
    body = sales_invoice_body(ctx["so"]["id"],
                              [(ctx["so_line_id"], str(qty), price)])
    ctx["response"] = api.create_sales_invoice(body, headers=ctx["headers"])


@then("the invoice should be issued for the sales order")
def invoice_issued(ctx):
    response = ctx["response"]
    assert response.status_code in (200, 201), response.text
    assert response.json()["salesOrderId"] == ctx["so"]["id"]
