import pytest
from box_ai_agents_toolkit import BoxClient

from config import AppConfig
from mcp_auth.auth_box_api import get_ccg_client, get_jwt_client, get_oauth_client
from server_context import BoxContext


class FakeRequestContext:
    """
    A fake request context class for testing purposes.
    This class simulates the request context that would be provided by the FastMCP server.
    """

    def __init__(self):
        # Try to use CCG or JWT authentication for tests, fallback to OAuth
        # CCG and JWT don't require manual authorization flow
        app_config = AppConfig.from_env()
        try:
            client = get_ccg_client(config=app_config.box_api)
        except (ValueError, Exception):
            try:
                client = get_jwt_client(config=app_config.box_api)
            except (ValueError, Exception):
                # Fallback to OAuth (requires manual authorization first)
                client = get_oauth_client(config=app_config.box_api)

        self.lifespan_context = BoxContext(client=client)


class FakeContext:
    """
    A fake context class for testing purposes.
    This class simulates the context that would be provided by the FastMCP server.
    """

    def __init__(self):
        self.request_context = FakeRequestContext()


@pytest.fixture(scope="module")
def box_client() -> BoxClient:
    # Try to use CCG or JWT authentication for tests, fallback to OAuth
    # CCG and JWT don't require manual authorization flow
    app_config = AppConfig.from_env()

    try:
        return get_ccg_client(config=app_config.box_api)
    except (ValueError, Exception):
        try:
            return get_jwt_client(config=app_config.box_api)
        except (ValueError, Exception):
            # Fallback to OAuth (requires manual authorization first)
            return get_oauth_client(config=app_config.box_api)


@pytest.fixture(scope="module")
def ctx():
    """
    Fixture to provide a Context object for testing.
    """
    ctx = FakeContext()
    return ctx
