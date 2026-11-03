import re

from playwright.sync_api import Locator, expect

from ui.pages.base_page import BasePage


# Moduł Ledger: zakładki Manual entry i Reversal
class LedgerPage(BasePage):
    path = "/ledger?tab=manual-entry"

    def open(self):
        super().open()
        expect(self.heading("Ledger")).to_be_visible()
        expect(self.page.get_by_role(
            "tab", name="Manual entry")).to_have_attribute(
            "aria-selected", "true")
        return self

    # wiersz tabeli zapisu (0 = pierwszy wiersz danych, bez nagłówka)
    def _line(self, index: int) -> Locator:
        return self.page.get_by_role("tabpanel").locator(
            "tbody tr").nth(index)

    # kwoty i memo w wierszu nie mają etykiet, więc wskazujemy je
    # kolejnością pól tekstowych: Debit, Credit, Memo
    def _fill_line(self, index: int, account: str, debit: str,
                   credit: str) -> None:
        line = self._line(index)
        field = line.get_by_role("combobox")
        field.click()
        field.fill(account)
        self.page.get_by_role(
            "option", name=re.compile(rf"^{re.escape(account)}\b")
        ).first.click()
        line.get_by_role("textbox").nth(0).fill(debit)
        line.get_by_role("textbox").nth(1).fill(credit)

    # zbilansowany zapis: Wn debit_account / Ma credit_account
    def post_manual_entry(self, memo: str, debit_account: str,
                          credit_account: str, amount: str) -> None:
        form = self.page.get_by_role("tabpanel")
        form.get_by_role("textbox", name="Memo", exact=True).fill(memo)
        self._fill_line(0, debit_account, amount, "")
        self._fill_line(1, credit_account, "", amount)
        form.get_by_role("button", name="Post entry").click()

    # numer zapisu odczytany z powiadomienia "Journal entry #N posted"
    def posted_entry_no(self) -> int:
        pattern = re.compile(r"Journal entry #(\d+) posted")
        toast = self.notification(pattern)
        expect(toast).to_be_visible()
        return int(pattern.search(toast.inner_text()).group(1))

    # zakładka Reversal: wczytanie zapisu po numerze i jego odwrócenie
    def reverse_entry(self, entry_no: int) -> None:
        self.page.get_by_role("tab", name="Reversal").click()
        form = self.page.get_by_role("tabpanel")
        form.get_by_role("textbox", name="Entry no.",
                         exact=True).fill(str(entry_no))
        form.get_by_role("button", name="Load", exact=True).click()
        expect(form.get_by_text(f"#{entry_no}", exact=True)).to_be_visible()
        form.get_by_role("button", name="Reverse entry").click()

    # numer zapisu odwracającego odczytany z powiadomienia
    def reversal_entry_no(self) -> int:
        pattern = re.compile(r"Reversed by entry #(\d+)")
        toast = self.notification(pattern)
        expect(toast).to_be_visible()
        return int(pattern.search(toast.inner_text()).group(1))