from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_file_representation import box_file_text_extract_tool


@pytest.mark.asyncio
async def test_box_file_text_extract_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/markdown",
                        "content": "# Document Title\n\nThis is the extracted markdown content.",
                    }
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert result["representations"]["entries"][0]["representation"] == "text/markdown"
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_plain_text():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/plain",
                        "content": "Plain text extracted from the file.",
                    }
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert result["representations"]["entries"][0]["representation"] == "text/plain"
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_multiple_representations():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/markdown",
                        "content": "# Title\n\nMarkdown content",
                    },
                    {
                        "representation": "text/plain",
                        "content": "Title\n\nPlain text content",
                    },
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert len(result["representations"]["entries"]) == 2
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_empty_content():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/plain",
                        "content": "",
                    }
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert result["representations"]["entries"][0]["content"] == ""
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_complex_markdown():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    complex_markdown = """# Main Title

## Section 1

This is a paragraph with **bold** and *italic* text.

### Subsection
- List item 1
- List item 2
- List item 3

## Section 2

```python
def hello():
    print("Hello, World!")
```

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
"""
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/markdown",
                        "content": complex_markdown,
                    }
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert complex_markdown in result["representations"]["entries"][0]["content"]
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_with_special_characters():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    content_with_special_chars = "Content with special characters: 日本語, éàç, café, ñ"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {
            "representations": {
                "entries": [
                    {
                        "representation": "text/plain",
                        "content": content_with_special_chars,
                    }
                ]
            }
        }
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert content_with_special_chars in result["representations"]["entries"][0]["content"]
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_no_representations():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {"representations": {"entries": []}}
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "representations" in result
        assert len(result["representations"]["entries"]) == 0
        mock_extract.assert_called_once_with("client", file_id)


@pytest.mark.asyncio
async def test_box_file_text_extract_tool_error_response():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_file_representation.box_file_text_extract") as mock_extract,
        patch("tools.box_tools_file_representation.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_extract.return_value = {"error": "File format not supported"}
        result = await box_file_text_extract_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "error" in result
        mock_extract.assert_called_once_with("client", file_id)
