from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import (auth_headers, create_item, create_vendor, po_body,
                         receive_goods)

# BDD-01 (TS-08, z krokami z TS-05, TS-06): pełny przebieg zamówienia
# zakupu; powiela API-10 (test_ts05), API-12 (test_ts06) i API-16 (test_ts08)
scenarios("features/ts08_purchase_order_to_receipt.feature")


@given("a new vendor and a new item")
def vendor_and_item(api, ctx):
    admin = auth_headers(api, "admin")
    ctx["vendor"] = create_vendor(api, admin)
    ctx["item"] = create_item(api, admin)


@when(parsers.parse(
    "I create a purchase order for {qty:d} units at {price} each"))
def create_purchase_order(api, ctx, qty, price):
    body = po_body(ctx["vendor"]["id"], [(ctx["item"]["id"], str(qty), price)])
    ctx["response"] = api.create_purchase_order(body, headers=ctx["headers"])


@then(parsers.parse(
    "the purchase order should be saved as a draft for the vendor "
    "with {lines:d} line"))
def purchase_order_saved_as_draft(ctx, lines):
    response = ctx["response"]
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["partnerId"] == ctx["vendor"]["id"]
    assert data["status"] == "DRAFT"
    assert len(data["lines"]) == lines
    ctx["po"] = data


@when("I confirm the purchase order")
def confirm_purchase_order(api, ctx):
    ctx["response"] = api.confirm_purchase_order(ctx["po"]["id"],
                                                 headers=ctx["headers"])


@then("the purchase order should be confirmed")
def purchase_order_confirmed(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "CONFIRMED"
    ctx["po"] = response.json()


@when(parsers.parse(
    "I receive {qty:d} units of the purchase order into stock"))
def receive_purchase_order(api, ctx, qty):
    ctx["response"] = receive_goods(api, ctx["headers"], ctx["po"], str(qty))


@then("the goods receipt should be posted")
def goods_receipt_posted(ctx):
    response = ctx["response"]
    assert response.status_code == 201, response.text
    assert response.json()["status"] == "POSTED"


@then("the purchase order should be received")
def purchase_order_received(api, ctx):
    fetched = api.get_purchase_order(ctx["po"]["id"],
                                     headers=ctx["headers"]).json()
    assert fetched["status"] == "RECEIVED"
