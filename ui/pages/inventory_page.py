import re

from playwright.sync_api import expect

from ui.pages.base_page import BasePage


# Zakładka Adjustments dla Inventory
class AdjustmentsPage(BasePage):
    path = "/inventory?tab=adjustments"

    # otwarcie strony i upewnienie się, że została ona wybrana
    def open(self):
        super().open()
        expect(self.page.get_by_role(
            "tab", name="Adjustments")).to_have_attribute(
            "aria-selected", "true")
        return self

    # pełen schemat tworzenia korekcji stanu dla zamówienia
    def post_adjustment(self, item_sku: str, qty_delta: str,
                        unit_cost: str,
                        reason: str) -> None:
        form = self.page.get_by_role("tabpanel")
        self.pick(form, "Item", item_sku)
        location = form.get_by_role("combobox", name="Location",
                                    exact=True)
        location.click()
        self.page.get_by_role("option", name=re.compile(
            r"\(Stock\)")).first.click()
        form.get_by_role("textbox", name="Quantity delta",
                         exact=True).fill(qty_delta)
        form.get_by_role("textbox", name="Unit cost", exact=True).fill(
            unit_cost)
        form.get_by_role("textbox", name="Reason", exact=True).fill(
            reason)
        form.get_by_role("button", name="Post adjustment").click()
