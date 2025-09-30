import pytest

from tools.box_tools_files import (
    box_download_file_tool,
    box_read_tool,
    box_upload_file_from_content_tool,
    box_upload_file_from_path_tool,
)


@pytest.mark.asyncio
async def test_box_read_tool(ctx):
    # HAB-1-01.docx = 1728677291168. This file must exists
    resp = await box_read_tool(ctx, "1728677291168")
    content = resp.get("content", "")
    error = resp.get("error", "")

    assert resp is not None
    assert isinstance(resp, dict)
    assert "HAB-1-01" in content
    assert error == ""


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_download_file_tool(ctx):
    # HAB-1-01.docx = 1728677291168. This file must exists
    # Invoice-A5555.txt = 1823610366483. This file must exists
    saved_path, file_content, mime_type = await box_download_file_tool(
        ctx, "1823610366483"
    )

    assert saved_path is None
    assert file_content is not None
    assert mime_type is not None
    assert len(file_content) > 0


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_upload_file_from_path_tool(ctx):
    # Upload a file from the local filesystem to Box
    # The file must exists in the local filesystem
    resp = await box_upload_file_from_path_tool(
        ctx, "tests/test_files/HAB-1-01.docx", "0"
    )
    assert resp is not None
    assert isinstance(resp, str)
    assert len(resp) > 0
    assert "HAB-1-01.docx" in resp


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_upload_file_from_content_tool(ctx):
    # Upload a file from content to Box
    resp = await box_upload_file_from_content_tool(
        ctx, "This is a test content", "test_upload_tool.txt", "0"
    )
    assert resp is not None
    assert isinstance(resp, str)
    assert len(resp) > 0
