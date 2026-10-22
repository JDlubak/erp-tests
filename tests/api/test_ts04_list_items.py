import pytest
from api.helpers import auth_headers, create_item

pytestmark = pytest.mark.api


# Czy świeżo utworzoną pozycję da się znaleźć w katalogu towarów:
# na liście, po id i po SKU
def test_get_items_list_and_details_by_id_and_sku(api):
    headers = auth_headers(api, "admin")
    created = create_item(api, headers)

    list_res = api.get_items(headers=headers)
    assert list_res.status_code == 200
    assert any(i["id"] == created["id"] for i in list_res.json())

    id_res = api.get_item(created["id"], headers=headers)
    assert id_res.status_code == 200
    assert id_res.json()["sku"] == created["sku"]

    sku_res = api.get_item_by_sku(created["sku"], headers=headers)
    assert sku_res.status_code == 200
    assert sku_res.json()["id"] == created["id"]


# Czy nieistniejąca pozycja zwraca 404
def test_get_nonexistent_item_returns_404(api):
    headers = auth_headers(api, "admin")
    response = api.get_item(9999999, headers=headers)
    assert response.status_code == 404
