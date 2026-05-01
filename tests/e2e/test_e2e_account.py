import os

import pytest

from dzengi_com_client import DzengiClient


@pytest.fixture(scope="module")
def demo_client():
    api_key = os.environ["DZENGI_API_KEY"]
    api_secret = os.environ["DZENGI_API_SECRET"]
    return DzengiClient(api_key=api_key, api_secret=api_secret, testnet=True)


@pytest.mark.e2e
def test_get_account_returns_dict(demo_client):
    result = demo_client.get_account()
    assert isinstance(result, dict), "get_account() must return a dict"


@pytest.mark.e2e
def test_get_account_has_balances(demo_client):
    result = demo_client.get_account()
    assert "balances" in result, "Response must contain 'balances' key"
    assert isinstance(result["balances"], list), "'balances' must be a list"


