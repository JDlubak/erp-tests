import pytest
from config import USERS

pytestmark = pytest.mark.api


# Czy poprawnymi danymi można sie zalogować oraz czy
# dostają oni accessToken
def test_login_returns_token(api):
    for user in USERS:
        response = api.login(user, user)
        assert response.status_code == 200
        assert response.json()["username"] == user
        assert response.json()["accessToken"].count(".") == 2


# Czy admin ma wszystkie role
def test_admin_has_all_roles(api):
    login_response = api.login("admin", "admin")
    token = login_response.json()["accessToken"]
    response = api.me(headers={"Authorization": f"Bearer {token}"})
    roles = response.json()["roles"]
    assert {"ADMIN", "ACCOUNTANT", "WAREHOUSE", "SALES"} <= set(roles)


# Czy sa zabezpieczenia an rozne metody logowania
@pytest.mark.parametrize(
    "username, password, expected_status, description",
    [
        ("admin", "admin", 200, "valid username + correct password"),
        ("admin", "wrong", 401,
         "valid username + incorrect password"),
        ("non_existent", "admin", 401,
         "non-existent username + password from another account"),
        ("non_existent", "anything", 401,
         "non-existent username + incorrect password"),
        ("", "admin", 400, "empty username + correct password"),
        ("admin", "", 400, "valid username + empty password"),
        ("", "", 400, "empty username + empty password"),
        ("   ", "admin", 400, "username with only spaces"),
    ],
)
def test_login_decision_table(api, username, password,
                              expected_status, description):
    response = api.login(username, password)

    assert response.status_code == expected_status, description
    if expected_status == 200:
        assert response.json()["accessToken"]
    else:
        assert "accessToken" not in response.text
