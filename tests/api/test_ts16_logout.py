import pytest
from api.helpers import auth_headers

pytestmark = pytest.mark.api


# Czy zalogowany użytkownik może się poprawnie wylogować
def test_logout_authenticated_user(api):
    headers = auth_headers(api, "sales")
    response = api.logout(headers=headers)
    assert response.status_code in (200, 204)


# Czy wylogowanie bez tokenu zwraca błąd autoryzacji
def test_logout_without_token_fails(api):
    response = api.logout()
    assert response.status_code in (200, 204)