from unittest.mock import MagicMock, patch

import pytest

from tools.box_tools_search import (
    box_search_folder_by_name_tool,
    box_search_tool,
)


@pytest.fixture
def mock_ctx():
    """Mock context fixture"""
    ctx = MagicMock()
    return ctx


@pytest.fixture
def mock_box_client():
    """Mock Box client fixture"""
    return MagicMock()


@pytest.fixture
def sample_search_results():
    """Sample search results fixture"""
    results = []
    for i in range(3):
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {
            "id": f"12345{i}",
            "name": f"test_file_{i}.pdf",
            "type": "file",
            "description": "Test file description",
            "size": 1024 + i * 100,
            "created_at": "2023-01-01T00:00:00Z",
        }
        results.append(mock_result)
    return results


@pytest.fixture
def sample_folder_results():
    """Sample folder search results fixture"""
    results = []
    for i in range(2):
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {
            "id": f"folder_12345{i}",
            "name": f"test_folder_{i}",
            "type": "folder",
            "description": "Test folder description",
            "item_count": 10 + i,
            "created_at": "2023-01-01T00:00:00Z",
        }
        results.append(mock_result)
    return results


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_basic(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with basic parameters"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(ctx=mock_ctx, query="test document")

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_search.assert_called_once_with(
        mock_box_client,
        "test document",
        None,  # file_extensions
        [],  # content_types (empty because where_to_look_for_query is None)
        None,  # ancestor_folder_ids
    )

    assert isinstance(result, list)
    assert len(result) == 3
    for i, item in enumerate(result):
        assert item["id"] == f"12345{i}"
        assert item["name"] == f"test_file_{i}.pdf"
        assert item["type"] == "file"


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_with_file_extensions(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with file extensions"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(
        ctx=mock_ctx, query="test document", file_extensions=["pdf", "docx"]
    )

    mock_search.assert_called_once_with(
        mock_box_client, "test document", ["pdf", "docx"], [], None
    )
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_with_content_types(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with content types"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(
        ctx=mock_ctx,
        query="test document",
        where_to_look_for_query=["NAME", "DESCRIPTION", "FILE_CONTENT"],
    )

    # Verify that the content types were converted correctly
    call_args = mock_search.call_args
    content_types_arg = call_args[0][3]  # Fourth argument is content_types
    assert len(content_types_arg) == 3
    # We can't easily test the enum values directly in the mock, but we can verify the call was made
    mock_search.assert_called_once()
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_with_ancestor_folders(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with ancestor folder IDs"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(
        ctx=mock_ctx,
        query="test document",
        ancestor_folder_ids=["folder_123", "folder_456"],
    )

    mock_search.assert_called_once_with(
        mock_box_client, "test document", None, [], ["folder_123", "folder_456"]
    )
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_all_parameters(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with all parameters"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(
        ctx=mock_ctx,
        query="test document",
        file_extensions=["pdf", "docx"],
        where_to_look_for_query=["NAME", "DESCRIPTION"],
        ancestor_folder_ids=["folder_123"],
    )

    mock_search.assert_called_once_with(
        mock_box_client,
        "test document",
        ["pdf", "docx"],
        mock_search.call_args[0][
            3
        ],  # content_types (converted from where_to_look_for_query)
        ["folder_123"],
    )
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_locate_folder_by_name")
async def test_box_search_folder_by_name_tool(
    mock_locate_folder,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_folder_results,
):
    """Test box_search_folder_by_name_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_locate_folder.return_value = sample_folder_results

    result = await box_search_folder_by_name_tool(
        ctx=mock_ctx, folder_name="test_folder"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_locate_folder.assert_called_once_with(mock_box_client, "test_folder")

    assert isinstance(result, list)
    assert len(result) == 2
    for i, item in enumerate(result):
        assert item["id"] == f"folder_12345{i}"
        assert item["name"] == f"test_folder_{i}"
        assert item["type"] == "folder"


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_empty_results(
    mock_search, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_search_tool function with empty results"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = []

    result = await box_search_tool(ctx=mock_ctx, query="nonexistent document")

    mock_search.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_locate_folder_by_name")
async def test_box_search_folder_by_name_tool_empty_results(
    mock_locate_folder, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_search_folder_by_name_tool function with empty results"""
    mock_get_client.return_value = mock_box_client
    mock_locate_folder.return_value = []

    result = await box_search_folder_by_name_tool(
        ctx=mock_ctx, folder_name="nonexistent_folder"
    )

    mock_locate_folder.assert_called_once_with(mock_box_client, "nonexistent_folder")
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_exception_handling(
    mock_search, mock_get_client, mock_ctx, mock_box_client
):
    """Test exception handling in box_search_tool"""
    mock_get_client.return_value = mock_box_client
    mock_search.side_effect = Exception("Search API Error")

    with pytest.raises(Exception) as exc_info:
        await box_search_tool(ctx=mock_ctx, query="test document")

    assert str(exc_info.value) == "Search API Error"


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_locate_folder_by_name")
async def test_box_search_folder_by_name_tool_exception_handling(
    mock_locate_folder, mock_get_client, mock_ctx, mock_box_client
):
    """Test exception handling in box_search_folder_by_name_tool"""
    mock_get_client.return_value = mock_box_client
    mock_locate_folder.side_effect = Exception("Folder search API Error")

    with pytest.raises(Exception) as exc_info:
        await box_search_folder_by_name_tool(ctx=mock_ctx, folder_name="test_folder")

    assert str(exc_info.value) == "Folder search API Error"


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_single_content_type(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with single content type"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(
        ctx=mock_ctx, query="test document", where_to_look_for_query=["NAME"]
    )

    call_args = mock_search.call_args
    content_types_arg = call_args[0][3]
    assert len(content_types_arg) == 1
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_empty_string_query(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with empty string query"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    result = await box_search_tool(ctx=mock_ctx, query="")

    mock_search.assert_called_once_with(mock_box_client, "", None, [], None)
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_search")
async def test_box_search_tool_special_characters_query(
    mock_search, mock_get_client, mock_ctx, mock_box_client, sample_search_results
):
    """Test box_search_tool function with special characters in query"""
    mock_get_client.return_value = mock_box_client
    mock_search.return_value = sample_search_results

    special_query = "test@file#123!.pdf"
    result = await box_search_tool(ctx=mock_ctx, query=special_query)

    mock_search.assert_called_once_with(mock_box_client, special_query, None, [], None)
    assert len(result) == 3


@pytest.mark.asyncio
@patch("tools.box_tools_search.get_box_client")
@patch("tools.box_tools_search.box_locate_folder_by_name")
async def test_box_search_folder_by_name_tool_special_characters(
    mock_locate_folder,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_folder_results,
):
    """Test box_search_folder_by_name_tool function with special characters in folder name"""
    mock_get_client.return_value = mock_box_client
    mock_locate_folder.return_value = sample_folder_results

    special_folder_name = "test_folder@123#"
    result = await box_search_folder_by_name_tool(
        ctx=mock_ctx, folder_name=special_folder_name
    )

    mock_locate_folder.assert_called_once_with(mock_box_client, special_folder_name)
    assert len(result) == 2
