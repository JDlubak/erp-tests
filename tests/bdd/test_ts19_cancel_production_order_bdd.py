from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import create_draft_wo, wo_location_body

# BDD-06 (TS-19): powiela API-37 (test_ts19_cancel_production_order.py)
scenarios("features/ts19_cancel_production_order.feature")


@given(parsers.parse("a released production order for {qty:d} units"))
def released_production_order(api, ctx, qty):
    _, ctx["wo"], ctx["loc_id"] = create_draft_wo(api, qty=str(qty))
    response = api.release_production_order(ctx["wo"]["id"],
                                            headers=ctx["headers"])
    assert response.status_code == 200, response.text


@when("I cancel the production order")
def cancel_production_order(api, ctx):
    ctx["response"] = api.cancel_production_order(
        ctx["wo"]["id"], wo_location_body(ctx["loc_id"]),
        headers=ctx["headers"])


@then("the production order should be cancelled")
def production_order_cancelled(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text
    assert response.json()["status"] in ("CANCELLED", "CANCELED")
