from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_users import (
    box_users_list_tool,
    box_users_locate_by_email_tool,
    box_users_locate_by_name_tool,
    box_users_search_by_name_or_email_tool,
)


@pytest.mark.asyncio
async def test_box_users_list_tool():
    ctx = MagicMock(spec=Context)
    with (
        patch("tools.box_tools_users.get_box_client") as mock_get_client,
        patch("tools.box_tools_users.box_users_list") as mock_list,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = [{"id": "1", "name": "Test User"}]
        result = await box_users_list_tool(ctx)
        assert isinstance(result, list)
        assert result[0]["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_users_locate_by_email_tool():
    ctx = MagicMock(spec=Context)
    email = "test@example.com"
    with (
        patch("tools.box_tools_users.get_box_client") as mock_get_client,
        patch("tools.box_tools_users.box_users_locate_by_email") as mock_locate,
    ):
        mock_get_client.return_value = "client"
        mock_locate.return_value = {"id": "1", "email": email}
        result = await box_users_locate_by_email_tool(ctx, email)
        assert isinstance(result, dict)
        assert result["email"] == email


@pytest.mark.asyncio
async def test_box_users_locate_by_name_tool():
    ctx = MagicMock(spec=Context)
    name = "Test User"
    with (
        patch("tools.box_tools_users.get_box_client") as mock_get_client,
        patch("tools.box_tools_users.box_users_locate_by_name") as mock_locate,
    ):
        mock_get_client.return_value = "client"
        mock_locate.return_value = {"id": "1", "name": name}
        result = await box_users_locate_by_name_tool(ctx, name)
        assert isinstance(result, dict)
        assert result["name"] == name


@pytest.mark.asyncio
async def test_box_users_search_by_name_or_email_tool():
    ctx = MagicMock(spec=Context)
    query = "Test"
    with (
        patch("tools.box_tools_users.get_box_client") as mock_get_client,
        patch("tools.box_tools_users.box_users_search_by_name_or_email") as mock_search,
    ):
        mock_get_client.return_value = "client"
        mock_search.return_value = [{"id": "1", "name": "Test User"}]
        result = await box_users_search_by_name_or_email_tool(ctx, query)
        assert isinstance(result, list)
        assert result[0]["name"] == "Test User"
