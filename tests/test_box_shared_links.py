import pytest
from unittest.mock import MagicMock, patch

from src.box_tools_shared_links import (
    box_shared_link_file_get_tool,
    box_shared_link_file_create_or_update_tool,
    box_shared_link_file_remove_tool,
    box_shared_link_file_find_by_shared_link_url_tool,
    box_shared_link_folder_get_tool,
    box_shared_link_folder_create_or_update_tool,
    box_shared_link_folder_remove_tool,
    box_shared_link_folder_find_by_shared_link_url_tool,
    box_shared_link_web_link_get_tool,
    box_shared_link_web_link_create_or_update_tool,
    box_shared_link_web_link_remove_tool,
    box_shared_link_web_link_find_by_shared_link_url_tool,
)

from mcp.server.fastmcp import Context


@pytest.mark.asyncio
async def test_box_shared_link_file_get_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("src.box_tools_shared_links.box_shared_link_file_get") as mock_get,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_get.return_value = {"id": "12345", "type": "file", "shared_link": {}}
        result = await box_shared_link_file_get_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_file_create_or_update_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_file_create_or_update"
        ) as mock_create_or_update,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create_or_update.return_value = {
            "id": "12345",
            "type": "file",
            "shared_link": {},
        }
        result = await box_shared_link_file_create_or_update_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_file_remove_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("src.box_tools_shared_links.box_shared_link_file_remove") as mock_remove,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {"id": "12345", "type": "file", "shared_link": None}
        result = await box_shared_link_file_remove_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is None


@pytest.mark.asyncio
async def test_box_shared_link_file_find_by_shared_link_url_tool():
    ctx = MagicMock(spec=Context)
    shared_link_url = "https://box.com/s/abcd1234"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_file_find_by_shared_link_url"
        ) as mock_find,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_find.return_value = {"id": "12345", "type": "file", "shared_link": {}}
        result = await box_shared_link_file_find_by_shared_link_url_tool(
            ctx, shared_link_url
        )
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is not None


@pytest.mark.asyncio
async def test_box_shared_link_folder_get_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("src.box_tools_shared_links.box_shared_link_folder_get") as mock_get,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_get.return_value = {"id": "12345", "type": "folder", "shared_link": {}}
        result = await box_shared_link_folder_get_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_folder_create_or_update_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_folder_create_or_update"
        ) as mock_create_or_update,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create_or_update.return_value = {
            "id": "12345",
            "type": "folder",
            "shared_link": {},
        }
        result = await box_shared_link_folder_create_or_update_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_folder_remove_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_folder_remove"
        ) as mock_remove,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {
            "id": "12345",
            "type": "folder",
            "shared_link": None,
        }
        result = await box_shared_link_folder_remove_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is None


@pytest.mark.asyncio
async def test_box_shared_link_folder_find_by_shared_link_url_tool():
    ctx = MagicMock(spec=Context)
    shared_link_url = "https://box.com/s/abcd1234"
    with (
        patch(
            "src.box_tools_shared_links."
            "box_shared_link_folder_find_by_shared_link_url"
        ) as mock_find,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_find.return_value = {"id": "12345", "type": "folder", "shared_link": {}}
        result = await box_shared_link_folder_find_by_shared_link_url_tool(
            ctx, shared_link_url
        )
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is not None


@pytest.mark.asyncio
async def test_box_shared_link_web_link_get_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "12345"
    with (
        patch("src.box_tools_shared_links.box_shared_link_web_link_get") as mock_get,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_get.return_value = {"id": "12345", "type": "web_link", "shared_link": {}}
        result = await box_shared_link_web_link_get_tool(ctx, web_link_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_web_link_create_or_update_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "12345"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_web_link_create_or_update"
        ) as mock_create_or_update,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create_or_update.return_value = {
            "id": "12345",
            "type": "web_link",
            "shared_link": {},
        }
        result = await box_shared_link_web_link_create_or_update_tool(ctx, web_link_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"


@pytest.mark.asyncio
async def test_box_shared_link_web_link_remove_tool():
    ctx = MagicMock(spec=Context)
    web_link_id = "12345"
    with (
        patch(
            "src.box_tools_shared_links.box_shared_link_web_link_remove"
        ) as mock_remove,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {
            "id": "12345",
            "type": "web_link",
            "shared_link": None,
        }
        result = await box_shared_link_web_link_remove_tool(ctx, web_link_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is None


@pytest.mark.asyncio
async def test_box_shared_link_web_link_find_by_shared_link_url_tool():
    ctx = MagicMock(spec=Context)
    shared_link_url = "https://box.com/s/abcd1234"
    with (
        patch(
            "src.box_tools_shared_links."
            "box_shared_link_web_link_find_by_shared_link_url"
        ) as mock_find,
        patch("src.box_tools_shared_links.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_find.return_value = {"id": "12345", "type": "web_link", "shared_link": {}}
        result = await box_shared_link_web_link_find_by_shared_link_url_tool(
            ctx, shared_link_url
        )
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        assert result["shared_link"] is not None
