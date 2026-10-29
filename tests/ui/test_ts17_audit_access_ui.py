import re

import pytest
from playwright.sync_api import expect

from ui.pages.app_shell import AppShell

pytestmark = pytest.mark.ui


# Czy dostęp do śledzenia audytu zależy od roli administratora
@pytest.mark.parametrize(
    "username, allowed",
    [
        ("admin", True),
        ("sales", False),
        ("warehouse", False),
        ("accountant", False),
        ("guest", False),
    ],
)
def test_audit_trail_access_depends_on_admin_role(page, sign_in_as,
                                                  username, allowed):
    sign_in_as(username)
    shell = AppShell(page).open()
    shell.expect_dashboard_for(username)

    if allowed:
        expect(shell.nav_link("Audit Trail")).to_be_visible()
    else:
        expect(shell.nav_link("Audit Trail")).to_have_count(0)

    page.goto("/audit")

    if allowed:
        expect(shell.heading("Audit Trail")).to_be_visible()
        expect(page.get_by_text(
            re.compile(r"\d+ records"))).to_be_visible()
    else:
        shell.expect_forbidden()
