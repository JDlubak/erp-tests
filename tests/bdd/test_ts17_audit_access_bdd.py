import re

from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

# BDD-07: powiela UI-11 (tests/ui/test_ts17_audit_access_ui.py)
scenarios("features/ts17_audit_access.feature")


@then(parsers.parse("the Audit Trail link should be {state}"))
def audit_trail_link_state(ctx, state):
    link = ctx["shell"].nav_link("Audit Trail")
    if state == "shown":
        expect(link).to_be_visible()
    elif state == "hidden":
        expect(link).to_have_count(0)
    else:
        raise ValueError(f"Nieznany stan linku: {state}")


@when("I go to the audit trail page")
def go_to_audit_trail_page(ui_page):
    ui_page.goto("/audit")


@then("I should see the audit records")
def see_audit_records(ui_page, ctx):
    expect(ctx["shell"].heading("Audit Trail")).to_be_visible()
    expect(ui_page.get_by_text(re.compile(r"\d+ records"))).to_be_visible()


@then("I should see an access denied page")
def see_access_denied_page(ctx):
    ctx["shell"].expect_forbidden()
