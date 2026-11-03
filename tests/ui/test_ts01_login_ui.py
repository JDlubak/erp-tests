import re

import pytest
from playwright.sync_api import expect

from ui.pages.app_shell import AppShell
from ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


# Czy poprawne dane w formularzu logowania wpuszczają na Dashboard
@pytest.mark.parametrize("username", ["admin", "warehouse", "guest"])
def test_login_form_opens_dashboard(page, username):
    login = LoginPage(page).open()
    login.expect_visible()

    login.sign_in(username, username)

    expect(page).not_to_have_url(re.compile(r"/login"))
    AppShell(page).expect_dashboard_for(username)


# Czy złe hasło lub nieistniejący login pokazują błąd
# i zostawiają użytkownika na stronie logowania
@pytest.mark.parametrize(
    "username, password, description",
    [
        ("admin", "wrong", "poprawny login + złe hasło"),
        ("non_existent", "admin", "nieistniejący login + cudze hasło"),
    ],
)
def test_login_with_invalid_credentials_shows_error(
        page, username, password, description):
    login = LoginPage(page).open()

    login.sign_in(username, password)

    login.expect_invalid_credentials_error()
    expect(page).to_have_url(re.compile(r"/login$"))
    login.expect_visible()
