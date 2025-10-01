from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_web_link import (
    box_web_link_create_tool,
    box_web_link_delete_by_id_tool,
    box_web_link_get_by_id_tool,
    box_web_link_update_by_id_tool,
)


@pytest.mark.asyncio
async def test_box_web_link_create_tool():
    ctx = MagicMock(spec=Context)
    url = "https://example.com"
    parent_folder_id = "12345"
    name = "Example Link"
    description = "An example web link"
    with (
        patch("tools.box_tools_web_link.box_web_link_create") as mock_create,
        patch("tools.box_tools_web_link.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "web_link", "name": name}
        result = await box_web_link_create_tool(
            ctx, url, parent_folder_id, name, description
        )
        assert isinstance(result, dict)
        assert result["name"] == name


@pytest.mark.asyncio
async def test_box_web_link_get_by_id_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "1"
    with (
        patch("tools.box_tools_web_link.box_web_link_get_by_id") as mock_get,
        patch("tools.box_tools_web_link.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_get.return_value = {
            "id": web_link_id,
            "type": "web_link",
            "name": "Example Link",
        }
        result = await box_web_link_get_by_id_tool(ctx, web_link_id)
        assert isinstance(result, dict)
        assert result["id"] == web_link_id


@pytest.mark.asyncio
async def test_box_web_link_update_by_id_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "1"
    url = "https://updated-example.com"
    parent_folder_id = "12345"
    name = "Updated Example Link"
    description = "An updated example web link"
    with (
        patch("tools.box_tools_web_link.box_web_link_update_by_id") as mock_update,
        patch("tools.box_tools_web_link.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_update.return_value = {
            "id": web_link_id,
            "type": "web_link",
            "name": name,
            "url": url,
            "description": description,
        }
        result = await box_web_link_update_by_id_tool(
            ctx, web_link_id, url, parent_folder_id, name, description
        )
        assert isinstance(result, dict)
        assert result["name"] == name
        assert result["url"] == url
        assert result["description"] == description


@pytest.mark.asyncio
async def test_box_web_link_delete_by_id_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "1"
    with (
        patch("tools.box_tools_web_link.box_web_link_delete_by_id") as mock_delete,
        patch("tools.box_tools_web_link.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_delete.return_value = {"status": "deleted"}
        result = await box_web_link_delete_by_id_tool(ctx, web_link_id)
        assert isinstance(result, dict)
        assert result["status"] == "deleted"
