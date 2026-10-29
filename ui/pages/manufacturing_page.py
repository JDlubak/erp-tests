import re

from playwright.sync_api import expect, Locator

from ui.pages.base_page import BasePage


class WorkOrdersPage(BasePage):
    path = "/manufacturing?tab=work-orders"

    def open(self):
        super().open()
        expect(self.heading("Manufacturing")).to_be_visible()
        return self

    def drawer(self, wo_number: str) -> Locator:
        return self.dialog(f"Work order {wo_number}")

    def open_order(self, wo_number: str) -> Locator:
        self.find_row(wo_number).click()
        drawer = self.drawer(wo_number)
        expect(drawer).to_be_visible()
        return drawer

    def release(self, wo_number: str) -> None:
        self.drawer(wo_number).get_by_role("button", name="Release",
                                           exact=True).click()

    def _action(self, wo_number: str, button: str,
                dialog_title: re.Pattern,
                location_code: str,
                qty_produced: str | None = None) -> None:
        self.drawer(wo_number).get_by_role("button", name=button,
                                           exact=True).click()
        modal = self.dialog(dialog_title)
        expect(modal).to_be_visible()
        location = modal.get_by_role("combobox", name=re.compile(
            r"^(Issue components from|Receive finished goods "
            r"into|Return components to)"))
        location.click()
        self.page.get_by_role(
            "option",
            name=re.compile(rf"^{re.escape(location_code)} ")).click()
        if qty_produced is not None:
            field = modal.get_by_role("textbox",
                                      name="Quantity produced",
                                      exact=True)
            field.fill(qty_produced)
        modal.get_by_role("button", name="Confirm", exact=True).click()

    def issue(self, wo_number: str, location_code: str) -> None:
        self._action(wo_number, "Issue",
                     re.compile("issue work order", re.I),
                     location_code)

    def complete(self, wo_number: str, location_code: str,
                 qty_produced: str) -> None:
        self._action(wo_number, "Complete",
                     re.compile("complete work order", re.I),
                     location_code, qty_produced)
