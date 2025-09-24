import pytest
from unittest.mock import MagicMock, patch

from src.box_tools_collaboration import (
    box_collaboration_file_group_by_group_id_tool,
    box_collaboration_file_user_by_user_id_tool,
    box_collaboration_file_user_by_user_login_tool,
    box_collaboration_folder_group_by_group_id_tool,
    box_collaboration_folder_user_by_user_id_tool,
    box_collaboration_folder_user_by_user_login_tool,
)

from mcp.server.fastmcp import Context


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_file_group_by_group_id")
async def test_box_collaboration_file_group_by_group_id_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_file_group_by_group_id_tool(ctx, "file1", "group1")
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_file_user_by_user_id")
async def test_box_collaboration_file_user_by_user_id_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_file_user_by_user_id_tool(ctx, "file1", "user1")
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_file_user_by_user_login")
async def test_box_collaboration_file_user_by_user_login_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_file_user_by_user_login_tool(
        ctx, "file1", "user@email.com"
    )
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_folder_group_by_group_id")
async def test_box_collaboration_folder_group_by_group_id_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_folder_group_by_group_id_tool(
        ctx, "folder1", "group1"
    )
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_folder_user_by_user_id")
async def test_box_collaboration_folder_user_by_user_id_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_folder_user_by_user_id_tool(
        ctx, "folder1", "user1"
    )
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}


@pytest.mark.asyncio
@patch("src.box_tools_collaboration.get_box_client")
@patch("src.box_tools_collaboration.box_collaboration_folder_user_by_user_login")
async def test_box_collaboration_folder_user_by_user_login_tool(mock_func, mock_client):
    ctx = MagicMock(spec=Context)
    mock_client.return_value = "client"
    mock_func.return_value = {"result": "ok"}
    result = await box_collaboration_folder_user_by_user_login_tool(
        ctx, "folder1", "user@email.com"
    )
    mock_client.assert_called_once_with(ctx)
    mock_func.assert_called_once()
    assert result == {"result": "ok"}
