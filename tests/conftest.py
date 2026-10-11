import pytest

from api.client import ApiClient


@pytest.fixture
def api() -> ApiClient:
    return ApiClient()
