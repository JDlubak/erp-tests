from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from ui.pages.app_shell import AppShell
from ui.pages.login_page import LoginPage

# BDD-04 (TS-01): powiela UI-01 i UI-02 (tests/ui/test_ts01_login_ui.py)
scenarios("features/ts01_login.feature")


@given("I am on the sign-in page")
def on_sign_in_page(ui_page, ctx):
    ctx["login"] = LoginPage(ui_page).open()
    ctx["login"].expect_visible()


@when(parsers.parse(
    'I sign in with username "{username}" and password "{password}"'))
def sign_in_with_form(ui_page, ctx, username, password):
    ctx["username"] = username
    ctx["shell"] = AppShell(ui_page)
    ctx["login"].sign_in(username, password)


@then("I should see the invalid credentials error")
def see_invalid_credentials_error(ctx):
    ctx["login"].expect_invalid_credentials_error()
