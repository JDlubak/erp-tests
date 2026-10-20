import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8081")
UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:4200")

USER_EMAIL = os.getenv("USER_EMAIL",
                       "customer@practicesoftwaretesting.com")
USER_PASSWORD = os.getenv("USER_PASSWORD", "welcome01")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL",
                        "admin@practicesoftwaretesting.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "welcome01")

USERS = ["admin", "sales", "warehouse", "accountant", "guest"]
EXPECTED_ROLES = {
    "admin": "ADMIN",
    "sales": "SALES",
    "warehouse": "WAREHOUSE",
    "accountant": "ACCOUNTANT",
}

