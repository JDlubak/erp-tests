import re

from playwright.sync_api import Locator, Page, expect


# Bazowa strona dla każdej innej w projekcie
class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    # Otwarcie adresu przypisanegodo danej strony
    def open(self):
        self.page.goto(self.path)
        return self

    # Zwrócenie bocznego paska nawigacyjnego
    @property
    def navbar(self) -> Locator:
        return self.page.locator(".mantine-AppShell-navbar")

    # Szukanie nagłówka o wskazanej nazwie
    def heading(self, name: str) -> Locator:
        return self.page.get_by_role("heading", name=name, exact=True)

    # Szukanie okna dialogowego
    def dialog(self, title: str | re.Pattern) -> Locator:
        return self.page.get_by_role("dialog", name=title)

    # Szukanie powiadomień na stronie
    def notification(self, text: str | re.Pattern) -> Locator:
        pattern = text if isinstance(text, re.Pattern) else re.compile(
            re.escape(text))
        return self.page.get_by_text(pattern).first

    # wyszukiwanie danego tekstu w szukanym zakresie z naciśnięciem
    def pick(self, scope: Locator, label: str, search: str) -> None:
        field = scope.get_by_role("combobox", name=label, exact=True)
        field.click()
        field.fill(search)
        option = self.page.get_by_role(
            "option", name=re.compile(re.escape(search))).first
        option.click()

    def row(self, text: str) -> Locator:
        return self.page.get_by_role("row").filter(has_text=text)

    # wyszukiwanie konkretnego wiersza z tabeli z paginacją
    def find_row(self, text: str) -> Locator:
        row = self.row(text)
        expect(
            self.page.locator(".mantine-Skeleton-root")).to_have_count(
            0)
        pagination = self.page.locator(".mantine-Pagination-root")
        if row.count() == 0 and pagination.count():
            numbers = [n.strip() for n in pagination.get_by_role(
                "button").all_inner_texts()]
            for number in [n for n in numbers if n.isdigit()]:
                button = pagination.get_by_role("button", name=number,
                                                exact=True)
                button.click()
                expect(button).to_have_attribute("data-active", "true")
                if row.count():
                    break
        expect(row).to_have_count(1)
        return row
