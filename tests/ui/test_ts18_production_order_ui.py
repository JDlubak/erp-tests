import pytest
from playwright.sync_api import expect

from api.helpers import create_draft_wo, location_code_by_id
from ui.pages.manufacturing_page import WorkOrdersPage

pytestmark = pytest.mark.ui


# Czy zlecenie produkcyjne przechodzi poprawnie
# przez cały cykl życia w fabryce
def test_work_order_goes_through_release_issue_complete(page, api,
                                                        sign_in_as):
    warehouse, wo, loc_id = create_draft_wo(api)
    number = wo["woNumber"]
    stock = location_code_by_id(api, warehouse, loc_id)
    sign_in_as("warehouse")
    orders = WorkOrdersPage(page).open()
    drawer = orders.open_order(number)
    expect(drawer.get_by_text("Draft", exact=True)).to_be_visible()

    orders.release(number)
    expect(orders.notification(
        "Work order released (BOM snapshotted)")).to_be_visible()
    expect(drawer.get_by_text("Released", exact=True)).to_be_visible()

    orders.issue(number, stock)
    expect(
        orders.notification("Components issued to WIP")).to_be_visible()
    expect(
        drawer.get_by_text("In progress", exact=True)).to_be_visible()

    orders.complete(number, stock, "5")
    expect(orders.notification(
        "Work order completed; finished goods "
        "received")).to_be_visible()
    expect(drawer.get_by_text("Done", exact=True)).to_be_visible()
    fetched = api.get_production_order(wo["id"],
                                       headers=warehouse).json()
    assert fetched["status"] == "DONE"
