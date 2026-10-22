import pytest
from api.helpers import create_draft_so

pytestmark = pytest.mark.api


# Czy potwierdzenie zamówienia sprzedaży zmienia status na CONFIRMED
def test_confirm_sales_order_changes_status(api):
    sales, so = create_draft_so(api)

    response = api.confirm_sales_order(so["id"], headers=sales)
    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"


# Czy ponowne potwierdzenie zamówienia sprzedaży zwraca błąd
def test_confirm_already_confirmed_sales_order_fails(api):
    sales, so = create_draft_so(api)
    api.confirm_sales_order(so["id"], headers=sales)

    second_response = api.confirm_sales_order(so["id"], headers=sales)
    assert second_response.status_code in (400, 409, 422)
