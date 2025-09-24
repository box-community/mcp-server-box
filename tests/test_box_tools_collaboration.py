import pytest
from unittest.mock import MagicMock, patch

from src.box_tools_collaboration import (
    box_collaboration_list_by_file_tool,
    box_collaboration_list_by_folder_tool,
    box_collaboration_delete_tool,
    box_collaboration_file_group_by_group_id_tool,
    box_collaboration_file_user_by_user_id_tool,
    box_collaboration_file_user_by_user_login_tool,
    box_collaboration_folder_group_by_group_id_tool,
    box_collaboration_folder_user_by_user_id_tool,
    box_collaboration_folder_user_by_user_login_tool,
)

from mcp.server.fastmcp import Context


@pytest.mark.asyncio
async def test_box_collaboration_list_by_file_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch(
            "src.box_tools_collaboration.box_collaborations_list_by_file"
        ) as mock_list,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = [{"id": "1", "type": "user", "name": "Test User"}]
        result = await box_collaboration_list_by_file_tool(ctx, file_id)
        assert isinstance(result, list)
        assert result[0]["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_collaboration_list_by_folder_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "67890"
    with (
        patch(
            "src.box_tools_collaboration.box_collaborations_list_by_folder"
        ) as mock_list,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = [{"id": "1", "type": "group", "name": "Test Group"}]
        result = await box_collaboration_list_by_folder_tool(ctx, folder_id)
        assert isinstance(result, list)
        assert result[0]["name"] == "Test Group"


@pytest.mark.asyncio
async def test_box_collaboration_delete_tool():
    ctx = MagicMock(spec=Context)
    collaboration_id = "54321"
    with (
        patch("src.box_tools_collaboration.box_collaboration_delete") as mock_delete,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_delete.return_value = None  # Deletion typically returns nothing
        result = await box_collaboration_delete_tool(ctx, collaboration_id)
        assert result is None  # Ensure the result is None after deletion


@pytest.mark.asyncio
async def test_box_collaboration_file_user_by_user_id_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    user_id = "67890"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_file_user_by_user_id"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "user", "name": "Test User"}
        result = await box_collaboration_file_user_by_user_id_tool(
            ctx, file_id, user_id
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_collaboration_file_user_by_user_login_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    user_login = "testuser"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_file_user_by_user_login"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "user", "name": "Test User"}
        result = await box_collaboration_file_user_by_user_login_tool(
            ctx, file_id, user_login
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_collaboration_file_group_by_group_id_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    group_id = "67890"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_file_group_by_group_id"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "group", "name": "Test Group"}
        result = await box_collaboration_file_group_by_group_id_tool(
            ctx, file_id, group_id
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test Group"


@pytest.mark.asyncio
async def test_box_collaboration_folder_user_by_user_id_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    user_id = "67890"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_folder_user_by_user_id"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "user", "name": "Test User"}
        result = await box_collaboration_folder_user_by_user_id_tool(
            ctx, folder_id, user_id
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_collaboration_folder_user_by_user_login_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    user_login = "testuser"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_folder_user_by_user_login"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "user", "name": "Test User"}
        result = await box_collaboration_folder_user_by_user_login_tool(
            ctx, folder_id, user_login
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_box_collaboration_folder_group_by_group_id_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    group_id = "67890"
    with (
        patch(
            "src.box_tools_collaboration.box_collaboration_folder_group_by_group_id"
        ) as mock_create,
        patch("src.box_tools_collaboration.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "1", "type": "group", "name": "Test Group"}
        result = await box_collaboration_folder_group_by_group_id_tool(
            ctx, folder_id, group_id
        )
        assert isinstance(result, dict)
        assert result["name"] == "Test Group"
