import base64
from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_file_transfer import (
    box_file_download_tool,
    box_file_upload_tool,
)


@pytest.mark.asyncio
async def test_box_file_download_tool_text():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        text_content = b"Hello, World!"
        mock_download.return_value = (None, text_content, "text/plain")
        result = await box_file_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["content"] == "Hello, World!"
        assert result["mime_type"] == "text/plain"
        mock_download.assert_called_once_with("client", file_id, False, None)


@pytest.mark.asyncio
async def test_box_file_download_tool_text_with_save():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    save_path = "/tmp/test.txt"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        text_content = b"Test content"
        mock_download.return_value = (save_path, text_content, "text/plain")
        result = await box_file_download_tool(ctx, file_id, save_file=True, save_path=save_path)
        assert isinstance(result, dict)
        assert result["path_saved"] == save_path
        assert result["content"] == "Test content"
        assert result["mime_type"] == "text/plain"
        mock_download.assert_called_once_with("client", file_id, True, save_path)


@pytest.mark.asyncio
async def test_box_file_download_tool_image():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        image_content = b"\x89PNG\r\n\x1a\n"  # PNG header
        mock_download.return_value = (None, image_content, "image/png")
        result = await box_file_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["mime_type"] == "image/png"
        assert result["content"] == base64.b64encode(image_content).decode()
        mock_download.assert_called_once_with("client", file_id, False, None)


@pytest.mark.asyncio
async def test_box_file_download_tool_image_with_save():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    save_path = "/tmp/test.png"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        image_content = b"\x89PNG\r\n\x1a\n"
        mock_download.return_value = (save_path, image_content, "image/png")
        result = await box_file_download_tool(ctx, file_id, save_file=True, save_path=save_path)
        assert isinstance(result, dict)
        assert result["path_saved"] == save_path
        assert result["mime_type"] == "image/png"
        assert result["content"] == base64.b64encode(image_content).decode()
        mock_download.assert_called_once_with("client", file_id, True, save_path)


@pytest.mark.asyncio
async def test_box_file_download_tool_binary():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        binary_content = b"\x00\x01\x02\x03"
        mock_download.return_value = (None, binary_content, "application/octet-stream")
        result = await box_file_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["mime_type"] == "application/octet-stream"
        assert result["content"] == base64.b64encode(binary_content).decode()
        mock_download.assert_called_once_with("client", file_id, False, None)


@pytest.mark.asyncio
async def test_box_file_download_tool_no_content():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_download.return_value = (None, None, "text/plain")
        result = await box_file_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert result["mime_type"] == "text/plain"
        assert "content" not in result
        mock_download.assert_called_once_with("client", file_id, False, None)


@pytest.mark.asyncio
async def test_box_file_download_tool_text_with_invalid_encoding():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_transfer.box_file_download") as mock_download,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        # Invalid UTF-8 sequence
        text_content = b"Hello \xff World"
        mock_download.return_value = (None, text_content, "text/plain")
        result = await box_file_download_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "content" in result
        # Should have replaced invalid characters
        assert result["content"] == "Hello \ufffd World"
        mock_download.assert_called_once_with("client", file_id, False, None)


@pytest.mark.asyncio
async def test_box_file_upload_tool_text():
    ctx = MagicMock(spec=Context)
    content = "Test file content"
    file_name = "test.txt"
    parent_folder_id = 67890
    with (
        patch("tools.box_tools_file_transfer.box_file_upload") as mock_upload,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_upload.return_value = {"id": "99999", "name": file_name}
        result = await box_file_upload_tool(ctx, content, file_name, parent_folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "99999"
        assert result["name"] == file_name
        mock_upload.assert_called_once_with("client", content, file_name, parent_folder_id)


@pytest.mark.asyncio
async def test_box_file_upload_tool_bytes():
    ctx = MagicMock(spec=Context)
    content = b"Binary file content"
    file_name = "test.bin"
    parent_folder_id = 67890
    with (
        patch("tools.box_tools_file_transfer.box_file_upload") as mock_upload,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_upload.return_value = {"id": "99999", "name": file_name}
        result = await box_file_upload_tool(ctx, content, file_name, parent_folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "99999"
        assert result["name"] == file_name
        mock_upload.assert_called_once_with("client", content, file_name, parent_folder_id)


@pytest.mark.asyncio
async def test_box_file_upload_tool_with_special_characters():
    ctx = MagicMock(spec=Context)
    content = "Content with special chars: 日本語, éàç"
    file_name = "test_special.txt"
    parent_folder_id = 67890
    with (
        patch("tools.box_tools_file_transfer.box_file_upload") as mock_upload,
        patch("tools.box_tools_file_transfer.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_upload.return_value = {"id": "99999", "name": file_name}
        result = await box_file_upload_tool(ctx, content, file_name, parent_folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "99999"
        assert result["name"] == file_name
        mock_upload.assert_called_once_with("client", content, file_name, parent_folder_id)
