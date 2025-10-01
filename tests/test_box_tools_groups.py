from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_groups import (
    box_groups_list_by_user_tool,
    box_groups_list_members_tool,
    box_groups_search_tool,
)


@pytest.mark.asyncio
async def test_box_groups_search_tool():
    ctx = MagicMock(spec=Context)
    query = "Test Group"
    with (
        patch("tools.box_tools_groups.box_groups_search") as mock_search,
        patch("tools.box_tools_groups.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_search.return_value = [{"id": "1", "name": query}]
        result = await box_groups_search_tool(ctx, query)
        assert isinstance(result, list)
        assert result[0]["name"] == query


@pytest.mark.asyncio
async def test_box_groups_list_members_tool():
    ctx = MagicMock(spec=Context)
    group_id = "12345"
    with (
        patch("tools.box_tools_groups.box_groups_list_members") as mock_list,
        patch("tools.box_tools_groups.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = [{"id": "1", "name": "Member User"}]
        result = await box_groups_list_members_tool(ctx, group_id)
        assert isinstance(result, list)
        assert result[0]["name"] == "Member User"


@pytest.mark.asyncio
async def test_box_groups_list_by_user_tool():
    ctx = MagicMock(spec=Context)
    user_id = "67890"
    with (
        patch("tools.box_tools_groups.box_groups_list_by_user") as mock_list,
        patch("tools.box_tools_groups.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = [{"id": "1", "name": "User Group"}]
        result = await box_groups_list_by_user_tool(ctx, user_id)
        assert isinstance(result, list)
        assert result[0]["name"] == "User Group"
