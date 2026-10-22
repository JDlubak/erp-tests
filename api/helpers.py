import uuid
from datetime import date


# Nagłówek z tokenem dla wskazanego konta (hasło == login)
def auth_headers(api, user):
    response = api.login(user, user)
    return {
        "Authorization": f"Bearer {response.json()['accessToken']}"}


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
                   "unitPrice": str(price)} for item_id, qty, price in
                  lines],
    }


# Nagłówki magazyniera oraz świeży dostawca i towar (utworzone przez admina)
def prepare(api):
    admin = auth_headers(api, "admin")
    warehouse = auth_headers(api, "warehouse")
    return warehouse, create_vendor(api, admin), create_item(api,
                                                             admin)


# Zamówienie w statusie DRAFT (1 linia: 10 szt. po 5.00); zwraca (nagłówki magazyniera, zamówienie)
def create_draft_po(api):
    warehouse, vendor, item = prepare(api)
    response = api.create_purchase_order(
        po_body(vendor["id"], [(item["id"], "10", "5.00")]),
        headers=warehouse)
    assert response.status_code == 201
    return warehouse, response.json()


# Zamówienie w statusie CONFIRMED; zwraca (nagłówki magazyniera, zamówienie)
def create_confirmed_po(api):
    warehouse, po = create_draft_po(api)
    response = api.confirm_purchase_order(po["id"], headers=warehouse)
    assert response.status_code == 200
    return warehouse, response.json()


# Dane przyjęcia towaru; lines to lista krotek (poLineId, qty)
def grn_body(po_id, location_id, lines):
    return {
        "purchaseOrderId": po_id,
        "stockLocationId": location_id,
        "postingDate": date.today().isoformat(),
        "lines": [{"poLineId": line_id, "qty": str(qty)}
                  for line_id, qty in lines],
    }


# Id lokalizacji danego typu (STOCK, VENDOR, ...) w seedowanym
# magazynie WH1
def location_id_by_type(api, headers, location_type,
                        warehouse_code="WH1"):
    warehouses = api.get_warehouses(headers=headers).json()
    warehouse = next(
        w for w in warehouses if w["code"] == warehouse_code)
    locations = api.get_locations(warehouse["id"],
                                  headers=headers).json()
    return next(l["id"] for l in locations if
                l["locationType"] == location_type)


# Id lokalizacji typu STOCK w seedowanym magazynie WH1
def stock_location_id(api, headers):
    return location_id_by_type(api, headers, "STOCK")


# Dane nowej pozycji z unikalnym SKU; extra nadpisuje wybrane pola
def item_body(**extra):
    suffix = unique()
    body = {"sku": f"SKU-{suffix}", "name": f"Item {suffix}",
            "itemType": "RAW", "uom": "EA"}
    body.update(extra)
    return body


# Przyjęcie towaru do lokalizacji STOCK dla pierwszej linii zamówienia
def receive_goods(api, headers, po, qty):
    location = stock_location_id(api, headers)
    body = grn_body(po["id"], location, [(po["lines"][0]["id"], qty)])
    return api.create_goods_receipt(body, headers=headers)


# Dane korekty stanu; dodatnia qty to nadwyżka, ujemna to strata
def adjustment_body(item_id, location_id, qty, unit_cost="5.00",
                    reason="Inwentaryzacja"):
    body = {"itemId": item_id, "locationId": location_id,
            "qtyDelta": str(qty), "unitCost": unit_cost, "reason": reason,
            "postingDate": date.today().isoformat()}
    return {key: value for key, value in body.items() if value is not None}


# Nagłówki magazyniera, świeża pozycja i lokalizacja STOCK
def prepare_adjustment(api):
    admin = auth_headers(api, "admin")
    warehouse = auth_headers(api, "warehouse")
    return (warehouse, create_item(api, admin),
            stock_location_id(api, warehouse))


# Ręczne księgowanie Wn 1010 (kasa) / Ma 3100 (kapitał) na podaną kwotę
def manual_entry_body(amount="100.00", memo="Księgowanie testowe"):
    return {
        "postingDate": date.today().isoformat(),
        "memo": memo,
        "lines": [
            {"accountCode": "1010", "debit": amount, "credit": "0"},
            {"accountCode": "3100", "debit": "0", "credit": amount},
        ],
    }


# Księguje ręczny zapis i zwraca jego dane
def post_manual_entry(api, headers, **kwargs):
    response = api.create_journal_entry(manual_entry_body(**kwargs),
                                        headers=headers)
    assert response.status_code == 201
    return response.json()
