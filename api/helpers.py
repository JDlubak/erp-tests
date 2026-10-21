"""Wspólne funkcje pomocnicze testów API (umieść w pakiecie api/ obok client.py).

Wszystkie wywołania HTTP idą przez metody ApiClient – tutaj tylko składamy dane i scenariusze.
"""
import uuid
from datetime import date


# Nagłówek z tokenem dla wskazanego konta (hasło == login)
def auth_headers(api, user):
    response = api.login(user, user)
    return {"Authorization": f"Bearer {response.json()['accessToken']}"}


# Unikalny sufiks, żeby dane testowe były niezależne
def unique():
    return uuid.uuid4().hex[:8].upper()


# Nowy dostawca (kontrahent z flagą vendor)
def create_vendor(api, headers):
    suffix = unique()
    response = api.create_partner(
        {"code": f"V-{suffix}", "name": f"Vendor {suffix}",
         "vendor": True, "customer": False}, headers=headers)
    assert response.status_code == 201
    return response.json()


# Nowy klient (kontrahent bez flagi vendor)
def create_customer(api, headers):
    suffix = unique()
    response = api.create_partner(
        {"code": f"C-{suffix}", "name": f"Customer {suffix}",
         "vendor": False, "customer": True}, headers=headers)
    assert response.status_code == 201
    return response.json()


# Nowa pozycja towarowa
def create_item(api, headers):
    suffix = unique()
    response = api.create_item(
        {"sku": f"SKU-{suffix}", "name": f"Item {suffix}",
         "itemType": "RAW", "uom": "EA"}, headers=headers)
    assert response.status_code == 201
    return response.json()


# Dane zamówienia zakupu; lines to lista krotek (itemId, qty, price)
def po_body(partner_id, lines, order_date=None):
    return {
        "partnerId": partner_id,
        "orderDate": (order_date or date.today()).isoformat(),
        "lines": [{"itemId": item_id, "qtyOrdered": str(qty),
                   "unitPrice": str(price)} for item_id, qty, price in lines],
    }


# Nagłówki magazyniera oraz świeży dostawca i towar (utworzone przez admina)
def prepare(api):
    admin = auth_headers(api, "admin")
    warehouse = auth_headers(api, "warehouse")
    return warehouse, create_vendor(api, admin), create_item(api, admin)


# Zamówienie w statusie DRAFT (1 linia: 10 szt. po 5.00); zwraca (nagłówki magazyniera, zamówienie)
def create_draft_po(api):
    warehouse, vendor, item = prepare(api)
    response = api.create_purchase_order(
        po_body(vendor["id"], [(item["id"], "10", "5.00")]), headers=warehouse)
    assert response.status_code == 201
    return warehouse, response.json()


# Zamówienie w statusie CONFIRMED; zwraca (nagłówki magazyniera, zamówienie)
def create_confirmed_po(api):
    warehouse, po = create_draft_po(api)
    response = api.confirm_purchase_order(po["id"], headers=warehouse)
    assert response.status_code == 200
    return warehouse, response.json()


# Id lokalizacji typu STOCK w seedowanym magazynie WH1
def stock_location_id(api, headers):
    warehouses = api.get_warehouses(headers=headers).json()
    wh1 = next(w for w in warehouses if w["code"] == "WH1")
    locations = api.get_locations(wh1["id"], headers=headers).json()
    return next(l["id"] for l in locations if l["locationType"] == "STOCK")


# Dane przyjęcia towaru; lines to lista krotek (poLineId, qty)
def grn_body(po_id, location_id, lines):
    return {
        "purchaseOrderId": po_id,
        "stockLocationId": location_id,
        "postingDate": date.today().isoformat(),
        "lines": [{"poLineId": line_id, "qty": str(qty)}
                  for line_id, qty in lines],
    }