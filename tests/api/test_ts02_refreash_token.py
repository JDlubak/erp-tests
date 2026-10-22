import pytest

pytestmark = pytest.mark.api


# Czy odświeżony token jest akceptowany przez zabezpieczony endpoint
def test_refreshed_token_is_accepted_by_protected_endpoint(api):
    api.login("accountant", "accountant")
    refresh_res = api.refresh()
    assert refresh_res.status_code == 200
    assert refresh_res.json()["roles"] == ["ACCOUNTANT"]
    token = refresh_res.json()["accessToken"]
    assert token.count(".") == 2

    response = api.me(headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "accountant"


# Czy niepoprawna wartość ciasteczka jest odrzucana
def test_refresh_with_invalid_cookie_returns_401(api):
    response = api.refresh("garbage")
    assert response.status_code == 401
    assert "accessToken" not in response.text
