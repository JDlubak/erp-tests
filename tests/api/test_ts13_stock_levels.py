import pytest
from api.helpers import auth_headers, prepare_stocked_item

pytestmark = pytest.mark.api


# Czy po przyjęciu towaru stan na rękę (on-hand) oraz lista statusów są poprawnie zwracane
def test_get_item_on_hand_and_stock_status(api):
    warehouse = auth_headers(api, "warehouse")
    item_id, _ = prepare_stocked_item(api, qty="10")

    on_hand_res = api.get_item_on_hand(item_id, headers=warehouse)
    assert on_hand_res.status_code == 200

    status_res = api.get_stock_status(headers=warehouse)
    assert status_res.status_code == 200
    assert isinstance(status_res.json(), list)
