import re

from playwright.sync_api import expect, Locator

from ui.pages.base_page import BasePage


# Zakładka Orders w module Purchasing
class PurchaseOrdersPage(BasePage):
    path = "/purchasing?tab=orders"

    def open(self):
        super().open()
        expect(self.heading("Purchasing")).to_be_visible()
        return self

    def create_order(self, vendor_code: str, item_sku: str, qty: str,
                     price: str) -> None:
        self.page.get_by_role("button",
                              name="New purchase order").first.click()
        dialog = self.dialog("New purchase order")
        self.pick(dialog, "Vendor", vendor_code)
        self.pick(dialog, "Item", item_sku)
        dialog.get_by_role("textbox", name="Qty", exact=True).fill(qty)
        dialog.get_by_role("textbox", name="Unit price",
                           exact=True).fill(price)
        dialog.get_by_role("button", name="Create", exact=True).click()

    # numer zamówienia odczytany z powiadomienia o utworzeniu
    def created_po_number(self) -> str:
        toast = self.notification(
            re.compile(r"Purchase order \S+ created"))
        expect(toast).to_be_visible()
        return re.search(r"Purchase order (\S+) created",
                         toast.inner_text()).group(1)

    def drawer(self, po_number: str) -> Locator:
        return self.dialog(f"Purchase order {po_number}")

    # otwarcie szuflady istniejącego zamówienia z listy
    def open_order(self, po_number: str) -> Locator:
        self.find_row(po_number).click()
        drawer = self.drawer(po_number)
        expect(drawer).to_be_visible()
        return drawer

    def confirm_order(self, po_number: str) -> None:
        self.drawer(po_number).get_by_role(
            "button", name="Confirm order").click()
