import pytest
from playwright.sync_api import expect

from api.helpers import auth_headers, unique
from ui.pages.masterdata_page import ItemsPage

pytestmark = pytest.mark.ui


# Czy administrator tworzy pozycję towarową modalem i czy trafia ona
# do tabeli oraz do bazy (odczyt API po SKU)
def test_admin_creates_item_through_form(page, api, sign_in_as):
    admin = auth_headers(api, "admin")
    suffix = unique()
    sku, name = f"SKU-{suffix}", f"Item UI {suffix}"
    sign_in_as("admin")
    items = ItemsPage(page).open()

    items.create_item(sku, name)

    expect(items.find_item_row(sku)).to_contain_text(name)
    response = api.get_item_by_sku(sku, headers=admin)
    assert response.status_code == 200
    created = response.json()
    assert created["sku"] == sku
    assert created["name"] == name
    assert created["itemType"] == "RAW"
    assert created["uom"] == "EA"