import re

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

import config
from api.helpers import auth_headers
from ui.pages.app_shell import AppShell
from ui.pages.login_page import LoginPage
from ui.session import sign_in_via_api


@pytest.fixture
def ctx() -> dict:
    return {}


@pytest.fixture(scope="session")
def base_url() -> str:
    return config.UI_BASE_URL


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-US",
            "viewport": {"width": 1440, "height": 900}}


@pytest.fixture
def ui_page(context, page):
    context.add_init_script(
        "localStorage.setItem('erp.locale', 'en');"
        "localStorage.setItem('erp.onboarding',"
        " JSON.stringify({completed: true, currentStep: 99}));")
    return page


@given(parsers.parse('I am signed in as "{account}"'))
def signed_in_via_ui(ui_page, context, base_url, ctx, account):
    sign_in_via_api(context, base_url, account)
    ctx["username"] = account


@given(parsers.parse('I am authenticated in the API as "{account}"'))
def authenticated_in_api(api, ctx, account):
    ctx["username"] = account
    ctx["headers"] = auth_headers(api, account)


@when("I open the dashboard")
def open_dashboard(ui_page, ctx):
    ctx["shell"] = AppShell(ui_page).open()


@then("I should see my dashboard")
def see_my_dashboard(ctx):
    ctx["shell"].expect_dashboard_for(ctx["username"])


@when("I sign out")
def sign_out(ctx):
    ctx["shell"].sign_out(ctx["username"])


@then("I should see the sign-in page")
def see_sign_in_page(ui_page):
    expect(ui_page).to_have_url(re.compile(r"/login$"))
    LoginPage(ui_page).expect_visible()


@then("I should be redirected to the sign-in page")
def redirected_to_sign_in_page(ui_page):
    expect(ui_page).to_have_url(re.compile(r"/login$"))
