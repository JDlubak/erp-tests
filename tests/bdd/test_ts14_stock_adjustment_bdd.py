from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import (adjustment_body, auth_headers, create_item,
                         stock_location_id)

# BDD-03 (TS-14): powiela API-27 i API-28 (test_ts14_stock_adjustment.py)
scenarios("features/ts14_stock_adjustment.feature")


@given("a new item with no stock")
def new_item_with_no_stock(api, ctx):
    ctx["item"] = create_item(api, auth_headers(api, "admin"))
    ctx["loc_id"] = stock_location_id(api, ctx["headers"])


@when(parsers.parse("I post a stock surplus of {qty:d} units"))
def post_surplus(api, ctx, qty):
    body = adjustment_body(ctx["item"]["id"], ctx["loc_id"], qty)
    ctx["response"] = api.create_stock_adjustment(body, headers=ctx["headers"])


@when(parsers.parse("I post a stock loss of {qty:d} units"))
def post_loss(api, ctx, qty):
    body = adjustment_body(ctx["item"]["id"], ctx["loc_id"], -qty,
                           unit_cost=None)
    ctx["response"] = api.create_stock_adjustment(body, headers=ctx["headers"])


@then("the adjustment should be posted")
def adjustment_posted(ctx):
    response = ctx["response"]
    assert response.status_code == 201, response.text
    assert response.json()["status"] == "POSTED"


@then("the adjustment should be rejected as exceeding the stock")
def adjustment_rejected(ctx):
    assert ctx["response"].status_code == 422


@then(parsers.parse("the item should have {qty:d} units on hand"))
def item_on_hand(api, ctx, qty):
    stock = api.get_item_on_hand(ctx["item"]["id"],
                                 headers=ctx["headers"]).json()
    assert float(stock["onHandQty"]) == qty
