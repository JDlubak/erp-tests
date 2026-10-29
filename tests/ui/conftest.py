import pytest

import config
from ui.session import sign_in_via_api


@pytest.fixture(scope="session")
def base_url() -> str:
    return config.UI_BASE_URL


# przygotowanie języka angielskiego i stałego rozmiaru okna
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-US",
            "viewport": {"width": 1440, "height": 900}}


# wymuszenie języka angielskiego i dezaktywacja samouczka
@pytest.fixture(autouse=True)
def _english_and_no_tour(context):
    context.add_init_script(
        "localStorage.setItem('erp.locale', 'en');"
        "localStorage.setItem('erp.onboarding',"
        " JSON.stringify({completed: true, currentStep: 99}));")


# udostępnienie testom wygodnej metody do logowania z wybraną rolą w tle
@pytest.fixture
def sign_in_as(context, base_url):
    def _sign_in(username: str) -> str:
        sign_in_via_api(context, base_url, username)
        return username

    return _sign_in
