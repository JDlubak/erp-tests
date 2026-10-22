import pytest
from api.helpers import auth_headers

pytestmark = pytest.mark.api


# Czy admin może odczytać dziennik audytu
def test_admin_can_read_audit_log(api):
    admin = auth_headers(api, "admin")

    response = api.get_audit_log(headers=admin)
    assert response.status_code == 200
    page = response.json()
    assert isinstance(page["content"], list)
    assert page["totalElements"] >= 1
    assert len(page["content"]) <= 50


# Czy tylko admin ma dostęp do dziennika (pozostałe konta dostają 403)
def test_non_admin_cannot_read_audit_log(api):
    for user in ["sales", "warehouse", "accountant", "guest"]:
        response = api.get_audit_log(headers=auth_headers(api, user))
        assert response.status_code == 403, user
