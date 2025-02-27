import pytest
from box_sdk_gen import BoxClient
from src.lib.box_authentication import get_ccg_client, get_oauth_client


@pytest.fixture
def box_client() -> BoxClient:
    # return get_ccg_client()
    return get_oauth_client()
