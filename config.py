import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8081")
UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:8081")

USERS = ["admin", "sales", "warehouse", "accountant", "guest"]
EXPECTED_ROLES = {
    "admin": "ADMIN",
    "sales": "SALES",
    "warehouse": "WAREHOUSE",
    "accountant": "ACCOUNTANT",
}
