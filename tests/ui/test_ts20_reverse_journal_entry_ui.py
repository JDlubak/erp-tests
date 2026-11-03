from datetime import date

import pytest

from api.helpers import auth_headers, unique
from ui.pages.ledger_page import LedgerPage

pytestmark = pytest.mark.ui


# Czy księgowy księguje zbilansowany zapis ręczny (Wn 6100 / Ma 1010)
# i może go od razu odwrócić w zakładce Reversal
def test_accountant_posts_and_reverses_manual_entry(page, api,
                                                    sign_in_as):
    accountant = auth_headers(api, "accountant")
    seed = api.create_journal_entry(
        {"postingDate": date.today().isoformat(),
         "memo": "Przygotowanie kont do testu UI",
         "lines": [{"accountCode": "6100", "debit": "1.00",
                    "credit": "0"},
                   {"accountCode": "1010", "debit": "0",
                    "credit": "1.00"}]}, headers=accountant)
    assert seed.status_code == 201
    sign_in_as("accountant")
    ledger = LedgerPage(page).open()

    ledger.post_manual_entry(f"UI zapis {unique()}", "6100", "1010",
                             "100.00")
    entry_no = ledger.posted_entry_no()
    original = api.get_journal_entry(entry_no, headers=accountant).json()
    assert original["status"] == "POSTED"
    assert float(original["totalDebit"]) == 100
    assert float(original["totalCredit"]) == 100

    ledger.reverse_entry(entry_no)

    reversal_no = ledger.reversal_entry_no()
    assert reversal_no > entry_no
    reversed_original = api.get_journal_entry(
        entry_no, headers=accountant).json()
    assert reversed_original["reversedByEntryNo"] == reversal_no
    reversal = api.get_journal_entry(reversal_no,
                                     headers=accountant).json()
    assert reversal["status"] == "POSTED"
    assert float(reversal["totalDebit"]) == 100
    assert float(reversal["totalCredit"]) == 100