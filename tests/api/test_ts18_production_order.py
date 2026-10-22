import pytest
from api.helpers import create_draft_wo, wo_complete_body, wo_location_body

pytestmark = pytest.mark.api


# Czy zlecenie produkcyjne można utworzyć, zwolnić (release), wydać
# surowiec (issue) i zakończyć (complete)
def test_release_and_complete_production_order(api):
    warehouse, wo, loc_id = create_draft_wo(api)

    release_res = api.release_production_order(wo["id"], headers=warehouse)
    assert release_res.status_code == 200, release_res.text
    assert release_res.json()["status"] in ("RELEASED", "IN_PROGRESS")

    issue_res = api.issue_production_order(
        wo["id"], wo_location_body(loc_id), headers=warehouse)
    assert issue_res.status_code == 200, issue_res.text

    complete_res = api.complete_production_order(
        wo["id"], wo_complete_body(loc_id, "5"), headers=warehouse)
    assert complete_res.status_code == 200, complete_res.text
    assert complete_res.json()["status"] == "DONE"


# Czy próba zakończenia niezwolnionego zlecenia zwraca błąd
# (body jest poprawne, więc błąd wynika ze stanu zlecenia, a nie z walidacji)
def test_complete_unreleased_production_order_fails(api):
    warehouse, wo, loc_id = create_draft_wo(api)

    complete_res = api.complete_production_order(
        wo["id"], wo_complete_body(loc_id, "5"), headers=warehouse)
    assert complete_res.status_code in (400, 409, 422)
