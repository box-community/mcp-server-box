from unittest.mock import MagicMock, patch

import pytest

from server_context import BoxContext
from tools.box_tools_generic import (
    box_authorize_app_tool,
    box_who_am_i,
    get_box_client,
)


@pytest.fixture
def mock_ctx():
    """Mock context fixture"""
    ctx = MagicMock()
    mock_request_context = MagicMock()
    mock_lifespan_context = MagicMock(spec=BoxContext)
    mock_request_context.lifespan_context = mock_lifespan_context
    ctx.request_context = mock_request_context
    return ctx


@pytest.fixture
def mock_box_client():
    """Mock Box client fixture"""
    return MagicMock()


@pytest.fixture
def sample_user_response():
    """Sample user response fixture"""
    return {
        "id": "12345",
        "name": "John Doe",
        "login": "john.doe@example.com",
        "type": "user",
    }


def test_get_box_client_success(mock_ctx, mock_box_client):
    """Test get_box_client function with valid client"""
    mock_ctx.request_context.lifespan_context.client = mock_box_client

    result = get_box_client(mock_ctx)

    assert result == mock_box_client


def test_get_box_client_none_client(mock_ctx):
    """Test get_box_client function with None client"""
    mock_ctx.request_context.lifespan_context.client = None

    with pytest.raises(RuntimeError) as exc_info:
        get_box_client(mock_ctx)

    assert str(exc_info.value) == "Box client is not initialized in the context."


@pytest.mark.asyncio
async def test_box_who_am_i(mock_ctx, mock_box_client, sample_user_response):
    """Test box_who_am_i function"""
    mock_ctx.request_context.lifespan_context.client = mock_box_client
    mock_user = MagicMock()
    mock_user.to_dict.return_value = sample_user_response
    mock_box_client.users.get_user_me.return_value = mock_user

    result = await box_who_am_i(mock_ctx)

    mock_box_client.users.get_user_me.assert_called_once()
    mock_user.to_dict.assert_called_once()
    assert result == sample_user_response
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    assert "login" in result
    assert "type" in result
    assert result["type"] == "user"


@pytest.mark.asyncio
async def test_box_who_am_i_with_none_client(mock_ctx):
    """Test box_who_am_i function with None client"""
    mock_ctx.request_context.lifespan_context.client = None

    with pytest.raises(RuntimeError) as exc_info:
        await box_who_am_i(mock_ctx)

    assert str(exc_info.value) == "Box client is not initialized in the context."


@pytest.mark.asyncio
@patch("tools.box_tools_generic.authorize_app")
async def test_box_authorize_app_tool_success(mock_authorize_app):
    """Test box_authorize_app_tool function with successful authorization"""
    mock_authorize_app.return_value = True

    result = await box_authorize_app_tool()

    mock_authorize_app.assert_called_once()
    assert result == "Box application authorized successfully"


@pytest.mark.asyncio
@patch("tools.box_tools_generic.authorize_app")
async def test_box_authorize_app_tool_failure(mock_authorize_app):
    """Test box_authorize_app_tool function with failed authorization"""
    mock_authorize_app.return_value = False

    result = await box_authorize_app_tool()

    mock_authorize_app.assert_called_once()
    assert result == "Box application not authorized"


@pytest.mark.asyncio
@patch("tools.box_tools_generic.authorize_app")
async def test_box_authorize_app_tool_none_return(mock_authorize_app):
    """Test box_authorize_app_tool function with None return"""
    mock_authorize_app.return_value = None

    result = await box_authorize_app_tool()

    mock_authorize_app.assert_called_once()
    assert result == "Box application not authorized"


@pytest.mark.asyncio
async def test_box_who_am_i_api_exception(mock_ctx, mock_box_client):
    """Test box_who_am_i function with API exception"""
    mock_ctx.request_context.lifespan_context.client = mock_box_client
    mock_box_client.users.get_user_me.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        await box_who_am_i(mock_ctx)

    assert str(exc_info.value) == "API Error"
    mock_box_client.users.get_user_me.assert_called_once()


@pytest.mark.asyncio
@patch("tools.box_tools_generic.authorize_app")
async def test_box_authorize_app_tool_exception(mock_authorize_app):
    """Test box_authorize_app_tool function with exception"""
    mock_authorize_app.side_effect = Exception("Authorization Error")

    with pytest.raises(Exception) as exc_info:
        await box_authorize_app_tool()

    assert str(exc_info.value) == "Authorization Error"
    mock_authorize_app.assert_called_once()


def test_get_box_client_with_different_context_structure():
    """Test get_box_client function with different context structure"""
    # Test edge case where context structure might be different
    ctx = MagicMock()
    mock_client = MagicMock()

    # Set up the nested structure
    ctx.request_context.lifespan_context.client = mock_client

    result = get_box_client(ctx)
    assert result == mock_client


@pytest.mark.asyncio
async def test_box_who_am_i_custom_user_data(mock_ctx, mock_box_client):
    """Test box_who_am_i function with custom user data"""
    mock_ctx.request_context.lifespan_context.client = mock_box_client

    custom_user_response = {
        "id": "98765",
        "name": "Jane Smith",
        "login": "jane.smith@company.com",
        "type": "user",
        "enterprise": {"id": "123", "name": "Test Enterprise"},
        "created_at": "2023-01-01T00:00:00Z",
    }

    mock_user = MagicMock()
    mock_user.to_dict.return_value = custom_user_response
    mock_box_client.users.get_user_me.return_value = mock_user

    result = await box_who_am_i(mock_ctx)

    assert result == custom_user_response
    assert result["id"] == "98765"
    assert result["name"] == "Jane Smith"
    assert result["enterprise"]["name"] == "Test Enterprise"
