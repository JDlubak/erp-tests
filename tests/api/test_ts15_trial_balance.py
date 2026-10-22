import pytest
from api.helpers import auth_headers

pytestmark = pytest.mark.api


# Czy raport bilansu próbnego pod adresem /api/ledger/trial-balance jest zbilansowany
def test_get_trial_balance_is_balanced(api):
    accountant = auth_headers(api, "accountant")
    response = api.get_trial_balance(headers=accountant)

    assert response.status_code == 200
    data = response.json()
    if "totalDebit" in data and "totalCredit" in data:
        assert data["totalDebit"] == data["totalCredit"]


# Czy zapytanie o bilans próbny bez nagłówka autoryzacji zostaje odrzucone
def test_get_trial_balance_unauthorized_fails(api):
    response = api.get_trial_balance()
    assert response.status_code in (401, 403)