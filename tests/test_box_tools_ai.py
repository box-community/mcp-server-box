from unittest.mock import MagicMock, patch

import pytest

from tools.box_tools_ai import (
    box_ai_ask_file_multi_tool,
    box_ai_ask_file_single_tool,
    box_ai_ask_hub_tool,
    box_ai_extract_freeform_tool,
    box_ai_extract_structured_enhanced_using_fields_tool,
    box_ai_extract_structured_enhanced_using_template_tool,
    box_ai_extract_structured_using_fields_tool,
    box_ai_extract_structured_using_template_tool,
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
def sample_ai_response():
    """Sample AI response fixture"""
    return {
        "answer": "This is a test response",
        "confidence": 0.95,
        "created_at": "2023-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_fields():
    """Sample fields for structured extraction"""
    return [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Person's name",
        },
        {
            "type": "date",
            "key": "date",
            "displayName": "Date",
            "description": "Document date",
        },
    ]


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_file_single")
async def test_box_ai_ask_file_single_tool(
    mock_ask_single, mock_get_client, mock_ctx, mock_box_client, sample_ai_response
):
    """Test box_ai_ask_file_single_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_ask_single.return_value = sample_ai_response

    result = await box_ai_ask_file_single_tool(
        ctx=mock_ctx,
        file_id="123456",
        prompt="What is this document about?",
        ai_agent_id="agent_123",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_ask_single.assert_called_once_with(
        mock_box_client,
        "123456",
        prompt="What is this document about?",
        ai_agent_id="agent_123",
    )
    assert result == sample_ai_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_file_single")
async def test_box_ai_ask_file_single_tool_no_agent(
    mock_ask_single, mock_get_client, mock_ctx, mock_box_client, sample_ai_response
):
    """Test box_ai_ask_file_single_tool function without ai_agent_id"""
    mock_get_client.return_value = mock_box_client
    mock_ask_single.return_value = sample_ai_response

    result = await box_ai_ask_file_single_tool(
        ctx=mock_ctx, file_id="123456", prompt="What is this document about?"
    )

    mock_ask_single.assert_called_once_with(
        mock_box_client,
        "123456",
        prompt="What is this document about?",
        ai_agent_id=None,
    )
    assert result == sample_ai_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_file_multi")
async def test_box_ai_ask_file_multi_tool(
    mock_ask_multi, mock_get_client, mock_ctx, mock_box_client, sample_ai_response
):
    """Test box_ai_ask_file_multi_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_ask_multi.return_value = sample_ai_response

    file_ids = ["123456", "789012"]
    result = await box_ai_ask_file_multi_tool(
        ctx=mock_ctx,
        file_ids=file_ids,
        prompt="Compare these documents",
        ai_agent_id="agent_123",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_ask_multi.assert_called_once_with(
        mock_box_client,
        file_ids,
        prompt="Compare these documents",
        ai_agent_id="agent_123",
    )
    assert result == sample_ai_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_hub")
async def test_box_ai_ask_hub_tool(
    mock_ask_hub, mock_get_client, mock_ctx, mock_box_client, sample_ai_response
):
    """Test box_ai_ask_hub_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_ask_hub.return_value = sample_ai_response

    result = await box_ai_ask_hub_tool(
        ctx=mock_ctx,
        hubs_id="hub_123",
        prompt="What's in this hub?",
        ai_agent_id="agent_123",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_ask_hub.assert_called_once_with(
        mock_box_client,
        "hub_123",
        prompt="What's in this hub?",
        ai_agent_id="agent_123",
    )
    assert result == sample_ai_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_hub")
async def test_box_ai_ask_hub_tool_int_id(
    mock_ask_hub, mock_get_client, mock_ctx, mock_box_client, sample_ai_response
):
    """Test box_ai_ask_hub_tool function with integer hub ID"""
    mock_get_client.return_value = mock_box_client
    mock_ask_hub.return_value = sample_ai_response

    result = await box_ai_ask_hub_tool(
        ctx=mock_ctx, hubs_id="123", prompt="What's in this hub?"
    )

    mock_ask_hub.assert_called_once_with(
        mock_box_client, "123", prompt="What's in this hub?", ai_agent_id=None
    )
    assert result == sample_ai_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_freeform")
async def test_box_ai_extract_freeform_tool(
    mock_extract_freeform, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_ai_extract_freeform_tool function"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"extracted_data": "sample data"}
    mock_extract_freeform.return_value = extract_response

    file_ids = ["123456", "789012"]
    result = await box_ai_extract_freeform_tool(
        ctx=mock_ctx,
        file_ids=file_ids,
        prompt="Extract names and dates",
        ai_agent_id="agent_123",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_extract_freeform.assert_called_once_with(
        mock_box_client,
        file_ids,
        prompt="Extract names and dates",
        ai_agent_id="agent_123",
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_structured_using_fields")
async def test_box_ai_extract_structured_using_fields_tool(
    mock_extract_fields, mock_get_client, mock_ctx, mock_box_client, sample_fields
):
    """Test box_ai_extract_structured_using_fields_tool function"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"name": "John Doe", "date": "2023-01-01"}
    mock_extract_fields.return_value = extract_response

    file_ids = ["123456"]
    result = await box_ai_extract_structured_using_fields_tool(
        ctx=mock_ctx, file_ids=file_ids, fields=sample_fields, ai_agent_id="agent_123"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_extract_fields.assert_called_once_with(
        mock_box_client, file_ids, sample_fields, ai_agent_id="agent_123"
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_structured_using_template")
async def test_box_ai_extract_structured_using_template_tool(
    mock_extract_template, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_ai_extract_structured_using_template_tool function"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"template_data": "extracted info"}
    mock_extract_template.return_value = extract_response

    file_ids = ["123456"]
    result = await box_ai_extract_structured_using_template_tool(
        ctx=mock_ctx,
        file_ids=file_ids,
        template_key="template_123",
        ai_agent_id="agent_123",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_extract_template.assert_called_once_with(
        mock_box_client, file_ids, "template_123", ai_agent_id="agent_123"
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_structured_enhanced_using_fields")
async def test_box_ai_extract_structured_enhanced_using_fields_tool(
    mock_extract_enhanced_fields,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_fields,
):
    """Test box_ai_extract_structured_enhanced_using_fields_tool function"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"enhanced_name": "John Doe", "enhanced_date": "2023-01-01"}
    mock_extract_enhanced_fields.return_value = extract_response

    file_ids = ["123456"]
    result = await box_ai_extract_structured_enhanced_using_fields_tool(
        ctx=mock_ctx, file_ids=file_ids, fields=sample_fields
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_extract_enhanced_fields.assert_called_once_with(
        mock_box_client, file_ids, sample_fields
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_structured_enhanced_using_template")
async def test_box_ai_extract_structured_enhanced_using_template_tool(
    mock_extract_enhanced_template, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_ai_extract_structured_enhanced_using_template_tool function"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"enhanced_template_data": "enhanced extracted info"}
    mock_extract_enhanced_template.return_value = extract_response

    file_ids = ["123456"]
    result = await box_ai_extract_structured_enhanced_using_template_tool(
        ctx=mock_ctx, file_ids=file_ids, template_key="template_123"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_extract_enhanced_template.assert_called_once_with(
        mock_box_client, file_ids, "template_123"
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_ask_file_single")
async def test_box_ai_ask_file_single_tool_exception_handling(
    mock_ask_single, mock_get_client, mock_ctx, mock_box_client
):
    """Test exception handling in box_ai_ask_file_single_tool"""
    mock_get_client.return_value = mock_box_client
    mock_ask_single.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        await box_ai_ask_file_single_tool(
            ctx=mock_ctx, file_id="123456", prompt="What is this document about?"
        )

    assert str(exc_info.value) == "API Error"


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_freeform")
async def test_box_ai_extract_freeform_tool_empty_file_list(
    mock_extract_freeform, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_ai_extract_freeform_tool with empty file list"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"message": "No files provided"}
    mock_extract_freeform.return_value = extract_response

    result = await box_ai_extract_freeform_tool(
        ctx=mock_ctx, file_ids=[], prompt="Extract data"
    )

    mock_extract_freeform.assert_called_once_with(
        mock_box_client, [], prompt="Extract data", ai_agent_id=None
    )
    assert result == extract_response


@pytest.mark.asyncio
@patch("tools.box_tools_ai.get_box_client")
@patch("tools.box_tools_ai.box_ai_extract_structured_using_fields")
async def test_box_ai_extract_structured_using_fields_tool_empty_fields(
    mock_extract_fields, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_ai_extract_structured_using_fields_tool with empty fields"""
    mock_get_client.return_value = mock_box_client
    extract_response = {"message": "No fields provided"}
    mock_extract_fields.return_value = extract_response

    result = await box_ai_extract_structured_using_fields_tool(
        ctx=mock_ctx, file_ids=["123456"], fields=[]
    )

    mock_extract_fields.assert_called_once_with(
        mock_box_client, ["123456"], [], ai_agent_id=None
    )
    assert result == extract_response
