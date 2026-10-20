import requests

import config


class ApiClient:
    def __init__(self, base_url: str = config.API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_products(self, **params) -> requests.Response:
        return self.session.get(self._url("/products"), params=params,
                                timeout=10)

    def get_product(self, product_id: str) -> requests.Response:
        return self.session.get(self._url(f"/products/{product_id}"),
                                timeout=10)

    def login(self, username, password):
        return self.session.post(self._url(f"/api/auth/login"),
                         json={"username": username, "password": password}, auth=False)

    def me(self, **kw):
        return self.session.get(self._url("/api/auth/me"), **kw)
