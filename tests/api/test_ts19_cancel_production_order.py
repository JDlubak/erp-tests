import pytest
from api.helpers import create_draft_wo, wo_complete_body, wo_location_body

pytestmark = pytest.mark.api


# Czy zwolnione zlecenie produkcyjne można anulować (odwrócenie stanu)
def test_cancel_released_production_order(api):
    warehouse, wo, loc_id = create_draft_wo(api)
    release_res = api.release_production_order(wo["id"], headers=warehouse)
    assert release_res.status_code == 200, release_res.text

    cancel_res = api.cancel_production_order(
        wo["id"], wo_location_body(loc_id), headers=warehouse)
    assert cancel_res.status_code == 200, cancel_res.text
    assert cancel_res.json()["status"] in ("CANCELLED", "CANCELED")


# Czy anulowanie zakończonego zlecenia produkcyjnego jest blokowane
def test_cancel_completed_production_order_fails(api):
    warehouse, wo, loc_id = create_draft_wo(api)
    assert api.release_production_order(
        wo["id"], headers=warehouse).status_code == 200
    issue_res = api.issue_production_order(
        wo["id"], wo_location_body(loc_id), headers=warehouse)
    assert issue_res.status_code == 200, issue_res.text
    complete_res = api.complete_production_order(
        wo["id"], wo_complete_body(loc_id, "5"), headers=warehouse)
    assert complete_res.status_code == 200, complete_res.text

    cancel_res = api.cancel_production_order(
        wo["id"], wo_location_body(loc_id), headers=warehouse)
    assert cancel_res.status_code in (400, 409, 422), cancel_res.text
