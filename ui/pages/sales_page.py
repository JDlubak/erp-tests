from playwright.sync_api import expect, Locator

from ui.pages.base_page import BasePage


class SalesOrdersPage(BasePage):
    path = "/sales?tab=orders"

    def open(self):
        super().open()
        expect(self.heading("Sales")).to_be_visible()
        return self

    def create_order(self, customer_code: str, item_sku: str, qty: str,
                     price: str) -> None:
        self.page.get_by_role("button",
                              name="New sales order").first.click()
        dialog = self.dialog("New sales order")
        self.pick(dialog, "Customer", customer_code)
        self.pick(dialog, "Item", item_sku)
        dialog.get_by_role("textbox", name="Qty", exact=True).fill(qty)
        dialog.get_by_role("textbox", name="Unit price",
                           exact=True).fill(price)
        dialog.get_by_role("button", name="Create", exact=True).click()

    def drawer(self, so_number: str) -> Locator:
        return self.dialog(f"Sales order {so_number}")

    def confirm_order(self, so_number: str) -> None:
        self.drawer(so_number).get_by_role("button",
                                           name="Confirm order").click()
