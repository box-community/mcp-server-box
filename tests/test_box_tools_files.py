from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_file import (
    box_file_copy_tool,
    box_file_delete_tool,
    box_file_info_tool,
    box_file_lock_tool,
    box_file_move_tool,
    box_file_rename_tool,
    box_file_retention_date_clear_tool,
    box_file_retention_date_set_tool,
    box_file_set_description_tool,
    box_file_set_download_company_tool,
    box_file_set_download_open_tool,
    box_file_set_download_reset_tool,
    box_file_tag_add_tool,
    box_file_tag_list_tool,
    box_file_tag_remove_tool,
    box_file_thumbnail_download_tool,
    box_file_thumbnail_url_tool,
    box_file_unlock_tool,
)


@pytest.mark.asyncio
async def test_box_file_info_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_info") as mock_info,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_info.return_value = {"id": "12345", "name": "test_file.txt"}
        result = await box_file_info_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        mock_info.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_copy_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    destination_folder_id = "67890"
    with (
        patch("tools.box_tools_file.box_file_copy") as mock_copy,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_copy.return_value = {"id": "999", "name": "test_file.txt"}
        result = await box_file_copy_tool(ctx, file_id, destination_folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "999"
        mock_copy.assert_called_once_with(
            "client", file_id, destination_folder_id, None, None
        )


@pytest.mark.asyncio
async def test_box_file_copy_tool_with_name_and_version():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    destination_folder_id = "67890"
    new_name = "new_file.txt"
    version_number = 2
    with (
        patch("tools.box_tools_file.box_file_copy") as mock_copy,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_copy.return_value = {"id": "999", "name": new_name}
        result = await box_file_copy_tool(
            ctx, file_id, destination_folder_id, new_name, version_number
        )
        assert isinstance(result, dict)
        assert result["name"] == new_name
        mock_copy.assert_called_once_with(
            "client", file_id, destination_folder_id, new_name, version_number
        )


@pytest.mark.asyncio
async def test_box_file_delete_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_delete") as mock_delete,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_delete.return_value = {"message": "File deleted"}
        result = await box_file_delete_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_delete.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_move_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    destination_folder_id = "67890"
    with (
        patch("tools.box_tools_file.box_file_move") as mock_move,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_move.return_value = {"id": "12345", "parent": {"id": "67890"}}
        result = await box_file_move_tool(ctx, file_id, destination_folder_id)
        assert isinstance(result, dict)
        mock_move.assert_called_once_with("client", file_id, destination_folder_id)


@pytest.mark.asyncio
async def test_box_file_rename_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    new_name = "renamed_file.txt"
    with (
        patch("tools.box_tools_file.box_file_rename") as mock_rename,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_rename.return_value = {"id": "12345", "name": new_name}
        result = await box_file_rename_tool(ctx, file_id, new_name)
        assert isinstance(result, dict)
        assert result["name"] == new_name
        mock_rename.assert_called_once_with("client", file_id, new_name)


@pytest.mark.asyncio
async def test_box_file_set_description_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    description = "Test file description"
    with (
        patch("tools.box_tools_file.box_file_set_description") as mock_desc,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_desc.return_value = {"id": "12345", "description": description}
        result = await box_file_set_description_tool(ctx, file_id, description)
        assert isinstance(result, dict)
        assert result["description"] == description
        mock_desc.assert_called_once_with("client", file_id, description)


@pytest.mark.asyncio
async def test_box_file_retention_date_set_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    retention_date = "2025-12-31T23:59:59Z"
    with (
        patch("tools.box_tools_file.box_file_retention_date_set") as mock_set,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_set.return_value = {"id": "12345", "retention_date": retention_date}
        result = await box_file_retention_date_set_tool(ctx, file_id, retention_date)
        assert isinstance(result, dict)
        # Verify that the datetime was parsed correctly
        expected_dt = datetime.fromisoformat("2025-12-31T23:59:59+00:00")
        mock_set.assert_called_once_with("client", file_id, expected_dt)


@pytest.mark.asyncio
async def test_box_file_retention_date_clear_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_retention_date_clear") as mock_clear,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_clear.return_value = {"id": "12345", "retention_date": None}
        result = await box_file_retention_date_clear_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_clear.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_lock_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_lock") as mock_lock,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_lock.return_value = {"id": "12345", "lock": {"type": "lock"}}
        result = await box_file_lock_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_lock.assert_called_once_with("client", file_id, None, None)


@pytest.mark.asyncio
async def test_box_file_lock_tool_with_expiration_and_download_prevention():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    lock_expires_at = "2025-12-31T23:59:59Z"
    is_download_prevented = True
    with (
        patch("tools.box_tools_file.box_file_lock") as mock_lock,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_lock.return_value = {"id": "12345", "lock": {"type": "lock"}}
        result = await box_file_lock_tool(
            ctx, file_id, lock_expires_at, is_download_prevented
        )
        assert isinstance(result, dict)
        # Verify datetime parsing
        expected_dt = datetime.fromisoformat("2025-12-31T23:59:59+00:00")
        mock_lock.assert_called_once_with(
            "client", file_id, expected_dt, is_download_prevented
        )


@pytest.mark.asyncio
async def test_box_file_unlock_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_unlock") as mock_unlock,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_unlock.return_value = {"id": "12345", "lock": None}
        result = await box_file_unlock_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_unlock.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_set_download_open_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_set_download_open") as mock_open,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_open.return_value = {"id": "12345", "can_download": "open"}
        result = await box_file_set_download_open_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_open.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_set_download_company_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_set_download_company") as mock_company,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_company.return_value = {"id": "12345", "can_download": "company"}
        result = await box_file_set_download_company_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_company.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_set_download_reset_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_set_download_reset") as mock_reset,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_reset.return_value = {"id": "12345", "can_download": None}
        result = await box_file_set_download_reset_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_reset.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_tag_list_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_tag_list") as mock_list,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = {"tags": ["important", "urgent"]}
        result = await box_file_tag_list_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_list.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_tag_add_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    tag = "important"
    with (
        patch("tools.box_tools_file.box_file_tag_add") as mock_add,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_add.return_value = {"id": "12345", "tags": ["important"]}
        result = await box_file_tag_add_tool(ctx, file_id, tag)
        assert isinstance(result, dict)
        mock_add.assert_called_once_with("client", file_id, tag)


@pytest.mark.asyncio
async def test_box_file_tag_remove_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    tag = "important"
    with (
        patch("tools.box_tools_file.box_file_tag_remove") as mock_remove,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {"id": "12345", "tags": []}
        result = await box_file_tag_remove_tool(ctx, file_id, tag)
        assert isinstance(result, dict)
        mock_remove.assert_called_once_with("client", file_id, tag)


@pytest.mark.asyncio
async def test_box_file_thumbnail_url_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_thumbnail_url") as mock_url,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_url.return_value = {"thumbnail_url": "https://example.com/thumb.png"}
        result = await box_file_thumbnail_url_tool(ctx, file_id)
        assert isinstance(result, dict)
        mock_url.assert_called_once_with(
            "client", file_id, None, None, None, None, None
        )


@pytest.mark.asyncio
async def test_box_file_thumbnail_url_tool_with_dimensions():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    extension = "jpg"
    min_height = 64
    min_width = 64
    max_height = 256
    max_width = 256
    with (
        patch("tools.box_tools_file.box_file_thumbnail_url") as mock_url,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_url.return_value = {"thumbnail_url": "https://example.com/thumb.jpg"}
        result = await box_file_thumbnail_url_tool(
            ctx, file_id, extension, min_height, min_width, max_height, max_width
        )
        assert isinstance(result, dict)
        mock_url.assert_called_once_with(
            "client", file_id, extension, min_height, min_width, max_height, max_width
        )


@pytest.mark.asyncio
async def test_box_file_thumbnail_download_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_thumbnail_download") as mock_download,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_download.return_value = {"content": b"binary_image_data"}
        result = await box_file_thumbnail_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "content" in result
        # Verify that binary content was base64 encoded
        assert isinstance(result["content"], str)
        mock_download.assert_called_once_with(
            "client", file_id, None, None, None, None, None
        )


@pytest.mark.asyncio
async def test_box_file_thumbnail_download_tool_with_dimensions():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    extension = "png"
    min_height = 32
    min_width = 32
    max_height = 128
    max_width = 128
    with (
        patch("tools.box_tools_file.box_file_thumbnail_download") as mock_download,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_download.return_value = {"content": b"png_image_data"}
        result = await box_file_thumbnail_download_tool(
            ctx, file_id, extension, min_height, min_width, max_height, max_width
        )
        assert isinstance(result, dict)
        assert isinstance(result["content"], str)
        mock_download.assert_called_once_with(
            "client", file_id, extension, min_height, min_width, max_height, max_width
        )


@pytest.mark.asyncio
async def test_box_file_thumbnail_download_tool_no_binary_content():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file.box_file_thumbnail_download") as mock_download,
        patch("tools.box_tools_file.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_download.return_value = {"error": "Thumbnail not available"}
        result = await box_file_thumbnail_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "error" in result
        mock_download.assert_called_once_with(
            "client", file_id, None, None, None, None, None
        )
