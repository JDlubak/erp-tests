import pytest
from api.helpers import auth_headers, create_draft_so

pytestmark = pytest.mark.api


# Czy można pobrać listę zamówień sprzedaży oraz szczegóły utworzonego zamówienia
def test_list_and_get_sales_order_details(api):
    sales, created_so = create_draft_so(api)

    list_res = api.get_sales_orders(headers=sales)
    assert list_res.status_code == 200
    assert any(o["id"] == created_so["id"] for o in list_res.json())

    detail_res = api.get_sales_order(created_so["id"], headers=sales)
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == created_so["id"]


# Czy pobranie nieistniejącego zamówienia sprzedaży zwraca 404
def test_get_nonexistent_sales_order_returns_404(api):
    sales = auth_headers(api, "sales")
    response = api.get_sales_order(9999999, headers=sales)
    assert response.status_code == 404
