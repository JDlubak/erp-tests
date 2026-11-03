import re

from playwright.sync_api import expect

from ui.pages.base_page import BasePage


# Zakładka Items w module Master Data
class ItemsPage(BasePage):
    path = "/masterdata?tab=items"

    def open(self):
        super().open()
        expect(self.heading("Master Data")).to_be_visible()
        return self

    # utworzenie pozycji modalem; typ i jednostka zostają domyślne
    def create_item(self, sku: str, name: str) -> None:
        self.page.get_by_role("button", name="New item").first.click()
        dialog = self.dialog("New item")
        expect(dialog).to_be_visible()
        dialog.get_by_role("textbox", name="SKU", exact=True).fill(sku)
        dialog.get_by_role("textbox", name="Name", exact=True).fill(name)
        dialog.get_by_role("button", name="Create", exact=True).click()
        expect(self.notification(
            re.compile(rf"Item {re.escape(sku)} created"))
        ).to_be_visible()
        expect(dialog).to_be_hidden()

    # Tabela pozycji nie ma wyszukiwarki i dzieli dane na strony po 25
    # wierszy
    def find_item_row(self, sku: str):
        expect(self.page.locator(
            ".mantine-Skeleton-root")).to_have_count(0)
        row = self.row(sku)
        pagination = self.page.locator(".mantine-Pagination-root")
        while True:
            try:
                expect(row).to_have_count(1, timeout=700)
                return row
            except AssertionError:
                next_page = pagination.locator("button").last
                if not pagination.count() or next_page.is_disabled():
                    expect(row).to_have_count(1)
                    return row
                next_page.click()