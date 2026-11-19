from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import create_draft_wo, wo_complete_body, wo_location_body

# BDD-06 (TS-18): powiela API-35 (test_ts18_production_order.py)
scenarios("features/ts18_production_order.feature")


@given(parsers.parse("a draft production order for {qty:d} units"))
def draft_production_order(api, ctx, qty):
    _, ctx["wo"], ctx["loc_id"] = create_draft_wo(api, qty=str(qty))


@when("I release the production order")
def release_production_order(api, ctx):
    ctx["response"] = api.release_production_order(ctx["wo"]["id"],
                                                   headers=ctx["headers"])


@then("the production order should be released")
def production_order_released(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text
    assert response.json()["status"] in ("RELEASED", "IN_PROGRESS")


@when("I issue the materials for the production order from stock")
def issue_production_materials(api, ctx):
    ctx["response"] = api.issue_production_order(
        ctx["wo"]["id"], wo_location_body(ctx["loc_id"]),
        headers=ctx["headers"])


@then("the materials should be issued")
def production_materials_issued(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text


@when(parsers.parse(
    "I complete the production order with {qty:d} units produced"))
def complete_production_order(api, ctx, qty):
    ctx["response"] = api.complete_production_order(
        ctx["wo"]["id"], wo_complete_body(ctx["loc_id"], str(qty)),
        headers=ctx["headers"])


@then("the production order should be done")
def production_order_done(ctx):
    response = ctx["response"]
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "DONE"
