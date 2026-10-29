import re

import pytest
from playwright.sync_api import expect

from ui.pages.app_shell import AppShell
from ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


# Czy wylogowanie rzeczywiście kończy sesję i chroni trasy
def test_logout_ends_session_and_protects_routes(page, sign_in_as):
    sign_in_as("sales")
    shell = AppShell(page).open()
    shell.expect_dashboard_for("sales")

    shell.sign_out("sales")

    login = LoginPage(page)
    expect(page).to_have_url(re.compile(r"/login$"))
    login.expect_visible()

    page.goto("/sales")
    expect(page).to_have_url(re.compile(r"/login$"))

    page.goto("/")
    expect(page).to_have_url(re.compile(r"/login$"))
    login.expect_visible()
