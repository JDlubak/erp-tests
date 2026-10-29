import pytest
from playwright.sync_api import expect

from ui.pages.app_shell import AppShell

pytestmark = pytest.mark.ui


# Czy gość nie może używać akcji zapisu
@pytest.mark.parametrize(
    "url, heading, hidden_button, notice",
    [
        ("/masterdata?tab=items", "Master Data", "New item", None),
        ("/purchasing?tab=orders", "Purchasing", "New purchase order",
         None),
        ("/sales?tab=orders", "Sales", "New sales order", None),
        ("/inventory?tab=adjustments", "Inventory", None,
         "Stock adjustments require the WAREHOUSE role."),
        ("/ledger?tab=manual-entry", "Ledger", None,
         "Manual journal entries require the ACCOUNTANT role."),
    ],
)
def test_guest_cannot_use_write_actions(page, sign_in_as, url, heading,
                                        hidden_button, notice):
    sign_in_as("guest")
    shell = AppShell(page)

    page.goto(url)

    expect(shell.heading(heading)).to_be_visible()
    expect(page.get_by_role("tabpanel")).to_be_visible()
    if hidden_button:
        expect(page.get_by_role("button",
                                name=hidden_button)).to_have_count(0)
    if notice:
        expect(page.get_by_text(notice)).to_be_visible()
