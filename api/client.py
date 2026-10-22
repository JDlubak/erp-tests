import requests

import config


class ApiClient:
    def __init__(self, base_url: str = config.API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    # ---- autoryzacja (TS-01, TS-02, TS-16) -------------------------------
    def login(self, username, password) -> requests.Response:
        return self.session.post(self._url("/api/auth/login"),
                                 json={"username": username,
                                       "password": password},
                                 timeout=10)

    def me(self, **kw) -> requests.Response:
        return self.session.get(self._url("/api/auth/me"), timeout=10, **kw)

    # ---- dane podstawowe: pozycje towarowe (TS-03, TS-04) -----------------
    def create_item(self, body: dict, headers=None) -> requests.Response:
        return self.session.post(self._url("/api/masterdata/items"),
                                 json=body, headers=headers, timeout=10)

    def get_items(self, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/masterdata/items"),
                                headers=headers, timeout=10)

    def get_item(self, item_id, headers=None) -> requests.Response:
        return self.session.get(self._url(f"/api/masterdata/items/{item_id}"),
                                headers=headers, timeout=10)

    def get_item_by_sku(self, sku: str, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/masterdata/items/by-sku"),
                                params={"sku": sku}, headers=headers,
                                timeout=10)

    # ---- dane podstawowe: kontrahenci -------------------------------------
    def create_partner(self, body: dict, headers=None) -> requests.Response:
        return self.session.post(self._url("/api/masterdata/partners"),
                                 json=body, headers=headers, timeout=10)

    # ---- zakupy: zamówienia zakupu (TS-05, TS-06, TS-07) --------------------
    def create_purchase_order(self, body: dict,
                              headers=None) -> requests.Response:
        return self.session.post(
            self._url("/api/purchasing/purchase-orders"),
            json=body, headers=headers, timeout=10)

    def get_purchase_order(self, po_id, headers=None) -> requests.Response:
        return self.session.get(
            self._url(f"/api/purchasing/purchase-orders/{po_id}"),
            headers=headers, timeout=10)

    def confirm_purchase_order(self, po_id, headers=None) -> requests.Response:
        return self.session.post(
            self._url(f"/api/purchasing/purchase-orders/{po_id}/confirm"),
            headers=headers, timeout=10)

    # ---- zakupy: przyjęcie towaru GRN (TS-08) ------------------------------
    def create_goods_receipt(self, body: dict,
                             headers=None) -> requests.Response:
        return self.session.post(
            self._url("/api/purchasing/goods-receipts"),
            json=body, headers=headers, timeout=10)

    # ---- dane podstawowe: magazyny i lokalizacje ---------------------------
    def get_warehouses(self, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/masterdata/warehouses"),
                                headers=headers, timeout=10)

    def get_locations(self, warehouse_id, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/masterdata/locations"),
                                params={"warehouseId": warehouse_id},
                                headers=headers, timeout=10)

    def get_purchase_orders(self, headers=None) -> requests.Response:
        return self.session.get(
            self._url("/api/purchasing/purchase-orders"),
            headers=headers, timeout=10)

    def get_goods_receipt(self, grn_id, headers=None) -> requests.Response:
        return self.session.get(
            self._url(f"/api/purchasing/goods-receipts/{grn_id}"),
            headers=headers, timeout=10)

    def get_goods_receipts(self, headers=None) -> requests.Response:
        return self.session.get(
            self._url("/api/purchasing/goods-receipts"),
            headers=headers, timeout=10)

    # ---- administracja: dziennik audytu (TS-17) ----------------------------
    def get_audit_log(self, headers=None, **params) -> requests.Response:
        return self.session.get(self._url("/api/audit"), params=params,
                                headers=headers, timeout=10)

    def post_audit_log(self, body: dict, headers=None) -> requests.Response:
        return self.session.post(self._url("/api/audit"), json=body,
                                 headers=headers, timeout=10)

    # ---- autoryzacja: odświeżanie tokena (TS-02) ---------------------------
    def refresh(self, refresh_cookie=None) -> requests.Response:
        """Bez argumentu używa ciasteczka zapisanego w sesji po logowaniu.
        Z argumentem wysyła podaną wartość ciasteczka (osobne żądanie, bez sesji)."""
        if refresh_cookie is None:
            return self.session.post(self._url("/api/auth/refresh"),
                                     timeout=10)
        return requests.post(self._url("/api/auth/refresh"),
                             headers={"Accept": "application/json",
                                      "Cookie": f"refresh_token={refresh_cookie}"},
                             timeout=10)

    def get_refresh_cookie(self):
        return self.session.cookies.get("refresh_token")

    # ---- magazyn: korekty stanów (TS-14) -----------------------------------
    def create_stock_adjustment(self, body: dict,
                                headers=None) -> requests.Response:
        return self.session.post(self._url("/api/inventory/adjustments"),
                                 json=body, headers=headers, timeout=10)

    def get_item_on_hand(self, item_id, headers=None) -> requests.Response:
        return self.session.get(
            self._url(f"/api/inventory/items/{item_id}/on-hand"),
            headers=headers, timeout=10)

    # ---- księga główna: księgowania ręczne i ich odwracanie (TS-20) ----------
    def create_journal_entry(self, body: dict,
                             headers=None) -> requests.Response:
        return self.session.post(self._url("/api/ledger/journal-entries"),
                                 json=body, headers=headers, timeout=10)

    def get_journal_entry(self, entry_no, headers=None) -> requests.Response:
        return self.session.get(
            self._url(f"/api/ledger/journal-entries/{entry_no}"),
            headers=headers, timeout=10)

    def reverse_journal_entry(self, entry_no, body=None,
                              headers=None) -> requests.Response:
        return self.session.post(
            self._url(f"/api/ledger/journal-entries/{entry_no}/reverse"),
            json=body, headers=headers, timeout=10)

    def get_trial_balance(self, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/ledger/trial-balance"),
                                headers=headers, timeout=10)

# ---- autoryzacja: wylogowanie (TS-16)
    def logout(self, headers=None) -> requests.Response:
        return self.session.post(self._url("/api/auth/logout"),
                                 headers=headers, timeout=10)

    # ---- magazyn: lista statusów towarów (TS-13)
    def get_stock_status(self, headers=None) -> requests.Response:
        return self.session.get(self._url(
            "/api/inventory/items-status"), headers=headers, timeout=10)

    # ---- sprzedaż: zamówienia sprzedaży (TS-09, TS-10, TS-11)
    def create_sales_order(self, body: dict,
                           headers=None) -> requests.Response:
        return self.session.post(self._url("/api/sales/sales-orders"),
                                 json=body, headers=headers, timeout=10)

    def get_sales_orders(self, headers=None) -> requests.Response:
        return self.session.get(self._url("/api/sales/sales-orders"),
                                headers=headers, timeout=10)

    def get_sales_order(self, so_id, headers=None) -> requests.Response:
        return self.session.get(
            self._url(f"/api/sales/sales-orders/{so_id}"),
            headers=headers, timeout=10)

    def confirm_sales_order(self, so_id,
                            headers=None) -> requests.Response:
        return self.session.post(
            self._url(f"/api/sales/sales-orders/{so_id}/confirm"),
            headers=headers, timeout=10)

    # ---- sprzedaż: wydania towaru i faktury (TS-12, TS-21)
    def create_shipment(self, body: dict,
                        headers=None) -> requests.Response:
        return self.session.post(self._url("/api/sales/deliveries"),
                                 json=body, headers=headers, timeout=10)

    def create_sales_invoice(self, body: dict,
                             headers=None) -> requests.Response:
        return self.session.post(self._url("/api/sales/sales-invoices"),
                                 json=body, headers=headers, timeout=10)

    # ---- produkcja: zlecenia produkcyjne (TS-18, TS-19)
    def create_production_order(self, body: dict,
                                headers=None) -> requests.Response:
        return self.session.post(
            self._url("/api/manufacturing/work-orders"),
            json=body, headers=headers, timeout=10)

    def release_production_order(self, order_id,
                                 headers=None) -> requests.Response:
        return self.session.post(self._url(
            f"/api/manufacturing/work-orders/{order_id}/release"),
                                 headers=headers, timeout=10)

    def complete_production_order(self, order_id, body: dict = None,
                                  headers=None) -> requests.Response:
        return self.session.post(self._url(
            f"/api/manufacturing/work-orders/{order_id}/complete"),
                                 json=body, headers=headers, timeout=10)

    def issue_production_order(self, order_id, body: dict,
                               headers=None) -> requests.Response:
        return self.session.post(self._url(
            f"/api/manufacturing/work-orders/{order_id}/issue"),
                                 json=body, headers=headers, timeout=10)

    def cancel_production_order(self, order_id, body: dict,
                                headers=None) -> requests.Response:
        return self.session.post(self._url(
            f"/api/manufacturing/work-orders/{order_id}/cancel"),
                                 json=body, headers=headers, timeout=10)

    def create_bom(self, body: dict, headers=None) -> requests.Response:
        return self.session.post(self._url("/api/manufacturing/boms"),
                                 json=body, headers=headers, timeout=10)
