import pytest
from api.helpers import auth_headers, item_body

pytestmark = pytest.mark.api


# Czy admin może utworzyć pozycję podając tylko wymagane pola
def test_create_item_with_required_fields_only(api):
    headers = auth_headers(api, "admin")
    body = item_body()

    response = api.create_item(body, headers=headers)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] > 0
    assert created["sku"] == body["sku"]
    assert created["name"] == body["name"]
    assert created["itemType"] == "RAW"
    assert created["uom"] == "EA"
    assert created["stocked"] is True


# Czy niepoprawne wartości pól są odrzucane
@pytest.mark.parametrize(
    "field, value, description",
    [
        ("sku", "", "pusty SKU"),
        ("name", "   ", "nazwa złożona ze spacji"),
        ("itemType", "GADGET", "nieznany typ pozycji"),
    ],
)
def test_create_item_invalid_value_returns_400(api, field, value,
                                               description):
    headers = auth_headers(api, "admin")

    response = api.create_item(item_body(**{field: value}),
                               headers=headers)
    assert response.status_code == 400, description
