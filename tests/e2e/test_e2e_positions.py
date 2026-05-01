import os

import pytest

from dzengi_com_client import DzengiClient


@pytest.fixture(scope="module")
def demo_client():
    api_key = os.environ["DZENGI_API_KEY"]
    api_secret = os.environ["DZENGI_API_SECRET"]
    return DzengiClient(api_key=api_key, api_secret=api_secret, testnet=True)


@pytest.mark.e2e
def test_get_positions_returns_list(demo_client):
    result = demo_client.get_positions()
    assert isinstance(result, list), "get_positions() must return a list"


@pytest.mark.e2e
def test_get_positions_items_have_position_id(demo_client):
    result = demo_client.get_positions()
    for position in result:
        assert "positionId" in position, "Each position must contain 'positionId' key"
