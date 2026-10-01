from api import health, products
from client import API_URL


def test_integrated_api_health():
    assert health() == {"status": "ok"}


def test_integrated_api_returns_seeded_products():
    result = products()
    assert isinstance(result, list)
    assert result


def test_integrated_api_filters_category():
    result = products("categoria inexistente")
    assert result == []


def test_client_has_configurable_api_url():
    assert API_URL.startswith("http")
