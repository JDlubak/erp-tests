from playwright.sync_api import BrowserContext


# Szybkie zalogowanie się do UI przez API dla przypadków
# nietestujących logowania
def sign_in_via_api(context: BrowserContext, base_url: str,
                    username: str, password: str | None = None) -> dict:
    response = context.request.post(
        f"{base_url.rstrip('/')}/api/auth/login",
        data={"username": username, "password": password or username},
    )
    assert response.ok, (f"Logowanie {username} przez API: "
                         f"{response.status}")
    return response.json()
