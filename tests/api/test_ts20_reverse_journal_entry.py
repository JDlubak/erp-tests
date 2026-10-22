import pytest
from api.helpers import auth_headers, post_manual_entry

pytestmark = pytest.mark.api


# Czy księgowy może odwrócić ręczne księgowanie
# i czy odwrócenie to nowy zapis POSTED o tych samych sumach
def test_reverse_manual_entry_creates_posted_mirror_entry(api):
    accountant = auth_headers(api, "accountant")
    original = post_manual_entry(api, accountant)

    response = api.reverse_journal_entry(original["entryNo"],
                                         headers=accountant)
    assert response.status_code == 201
    reversal = response.json()
    assert reversal["status"] == "POSTED"
    assert reversal["entryNo"] > original["entryNo"]
    assert float(reversal["totalDebit"]) == float(original["totalDebit"]) == 100
    assert float(reversal["totalCredit"]) == float(original["totalCredit"]) == 100


# Czy tego samego księgowania nie można odwrócić dwa razy
def test_reverse_already_reversed_entry_returns_422(api):
    accountant = auth_headers(api, "accountant")
    original = post_manual_entry(api, accountant)
    api.reverse_journal_entry(original["entryNo"], headers=accountant)

    response = api.reverse_journal_entry(original["entryNo"],
                                         headers=accountant)
    assert response.status_code == 422

    detail = api.get_journal_entry(original["entryNo"],
                                   headers=accountant).json()
    assert detail["reversedByEntryNo"] is not None
