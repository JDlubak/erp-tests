from pytest_bdd import given, parsers, scenarios, then, when

from api.helpers import post_manual_entry

# BDD-02 (TS-20): powiela API-39 i API-40 (test_ts20_reverse_journal_entry.py)
scenarios("features/ts20_reverse_journal_entry.feature")


@given(parsers.parse("a manual journal entry of {amount}"))
def manual_journal_entry(api, ctx, amount):
    ctx["entry"] = post_manual_entry(api, ctx["headers"], amount=amount)


@when("I reverse the journal entry")
def reverse_journal_entry(api, ctx):
    ctx["response"] = api.reverse_journal_entry(ctx["entry"]["entryNo"],
                                                headers=ctx["headers"])


@then("a posted reversal with the same totals should be created")
def reversal_created(ctx):
    response = ctx["response"]
    assert response.status_code == 201, response.text
    reversal = response.json()
    assert reversal["status"] == "POSTED"
    assert reversal["entryNo"] > ctx["entry"]["entryNo"]
    assert float(reversal["totalDebit"]) == float(ctx["entry"]["totalDebit"])
    assert float(reversal["totalCredit"]) == float(
        ctx["entry"]["totalCredit"])


@then("the reversal should be rejected as already reversed")
def reversal_rejected(api, ctx):
    assert ctx["response"].status_code == 422
    detail = api.get_journal_entry(ctx["entry"]["entryNo"],
                                   headers=ctx["headers"]).json()
    assert detail["reversedByEntryNo"] is not None
