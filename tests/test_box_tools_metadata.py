from unittest.mock import MagicMock, patch

import pytest

from tools.box_tools_metadata import (
    box_metadata_delete_instance_on_file_tool,
    box_metadata_get_instance_on_file_tool,
    box_metadata_set_instance_on_file_tool,
    box_metadata_template_create_tool,
    box_metadata_template_get_by_key_tool,
    box_metadata_template_get_by_name_tool,
    box_metadata_update_instance_on_file_tool,
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
def sample_template_fields():
    """Sample template fields fixture"""
    return [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "The customer name",
            "hidden": False,
        },
        {
            "type": "date",
            "key": "last_contacted_at",
            "displayName": "Last Contacted At",
            "description": "When this customer was last contacted at",
            "hidden": False,
        },
        {
            "type": "enum",
            "key": "industry",
            "displayName": "Industry",
            "options": [{"key": "Technology"}, {"key": "Healthcare"}, {"key": "Legal"}],
        },
    ]


@pytest.fixture
def sample_metadata():
    """Sample metadata instance fixture"""
    return {
        "name": "John Doe",
        "last_contacted_at": "2023-01-01T00:00:00.000Z",
        "industry": "Technology",
    }


@pytest.fixture
def sample_template_response():
    """Sample template response fixture"""
    return {
        "id": "template_123",
        "templateKey": "customer_template",
        "displayName": "Customer Template",
        "fields": [{"type": "string", "key": "name", "displayName": "Name"}],
    }


@pytest.fixture
def sample_metadata_instance_response():
    """Sample metadata instance response fixture"""
    return {
        "$parent": "file_123456",
        "$template": "customer_template",
        "extra_data": {"name": "John Doe", "industry": "Technology"},
    }


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_create")
async def test_box_metadata_template_create_tool(
    mock_create,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_template_fields,
    sample_template_response,
):
    """Test box_metadata_template_create_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_create.return_value = sample_template_response

    result = await box_metadata_template_create_tool(
        ctx=mock_ctx,
        display_name="Customer Template",
        fields=sample_template_fields,
        template_key="customer_template",
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_create.assert_called_once_with(
        mock_box_client,
        "Customer Template",
        sample_template_fields,
        template_key="customer_template",
    )
    assert result == sample_template_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_create")
async def test_box_metadata_template_create_tool_no_key(
    mock_create,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_template_fields,
    sample_template_response,
):
    """Test box_metadata_template_create_tool function without template_key"""
    mock_get_client.return_value = mock_box_client
    mock_create.return_value = sample_template_response

    result = await box_metadata_template_create_tool(
        ctx=mock_ctx, display_name="Customer Template", fields=sample_template_fields
    )

    mock_create.assert_called_once_with(
        mock_box_client, "Customer Template", sample_template_fields, template_key=None
    )
    assert result == sample_template_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_get_by_key")
async def test_box_metadata_template_get_by_key_tool(
    mock_get_by_key,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_template_response,
):
    """Test box_metadata_template_get_by_key_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_get_by_key.return_value = sample_template_response

    result = await box_metadata_template_get_by_key_tool(
        ctx=mock_ctx, template_name="customer_template"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_get_by_key.assert_called_once_with(mock_box_client, "customer_template")
    assert result == sample_template_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_get_by_name")
async def test_box_metadata_template_get_by_name_tool(
    mock_get_by_name,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_template_response,
):
    """Test box_metadata_template_get_by_name_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_get_by_name.return_value = sample_template_response

    result = await box_metadata_template_get_by_name_tool(
        ctx=mock_ctx, template_name="Customer Template"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_get_by_name.assert_called_once_with(mock_box_client, "Customer Template")
    assert result == sample_template_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_set_instance_on_file")
async def test_box_metadata_set_instance_on_file_tool(
    mock_set_instance,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_metadata,
    sample_metadata_instance_response,
):
    """Test box_metadata_set_instance_on_file_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_set_instance.return_value = sample_metadata_instance_response

    result = await box_metadata_set_instance_on_file_tool(
        ctx=mock_ctx,
        template_key="customer_template",
        file_id="123456",
        metadata=sample_metadata,
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_set_instance.assert_called_once_with(
        mock_box_client, "customer_template", "123456", sample_metadata
    )
    assert result == sample_metadata_instance_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_get_instance_on_file")
async def test_box_metadata_get_instance_on_file_tool(
    mock_get_instance,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_metadata_instance_response,
):
    """Test box_metadata_get_instance_on_file_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_get_instance.return_value = sample_metadata_instance_response

    result = await box_metadata_get_instance_on_file_tool(
        ctx=mock_ctx, file_id="123456", template_key="customer_template"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_get_instance.assert_called_once_with(
        mock_box_client, "123456", "customer_template"
    )
    assert result == sample_metadata_instance_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_update_instance_on_file")
async def test_box_metadata_update_instance_on_file_tool(
    mock_update_instance,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_metadata,
    sample_metadata_instance_response,
):
    """Test box_metadata_update_instance_on_file_tool function"""
    mock_get_client.return_value = mock_box_client
    mock_update_instance.return_value = sample_metadata_instance_response

    result = await box_metadata_update_instance_on_file_tool(
        ctx=mock_ctx,
        file_id="123456",
        template_key="customer_template",
        metadata=sample_metadata,
        remove_non_included_data=True,
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_update_instance.assert_called_once_with(
        mock_box_client,
        "123456",
        "customer_template",
        sample_metadata,
        remove_non_included_data=True,
    )
    assert result == sample_metadata_instance_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_update_instance_on_file")
async def test_box_metadata_update_instance_on_file_tool_default_remove(
    mock_update_instance,
    mock_get_client,
    mock_ctx,
    mock_box_client,
    sample_metadata,
    sample_metadata_instance_response,
):
    """Test box_metadata_update_instance_on_file_tool function with default remove_non_included_data"""
    mock_get_client.return_value = mock_box_client
    mock_update_instance.return_value = sample_metadata_instance_response

    result = await box_metadata_update_instance_on_file_tool(
        ctx=mock_ctx,
        file_id="123456",
        template_key="customer_template",
        metadata=sample_metadata,
    )

    mock_update_instance.assert_called_once_with(
        mock_box_client,
        "123456",
        "customer_template",
        sample_metadata,
        remove_non_included_data=False,
    )
    assert result == sample_metadata_instance_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_delete_instance_on_file")
async def test_box_metadata_delete_instance_on_file_tool(
    mock_delete_instance, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_delete_instance_on_file_tool function"""
    mock_get_client.return_value = mock_box_client
    delete_response = {"message": "Metadata instance deleted successfully"}
    mock_delete_instance.return_value = delete_response

    result = await box_metadata_delete_instance_on_file_tool(
        ctx=mock_ctx, file_id="123456", template_key="customer_template"
    )

    mock_get_client.assert_called_once_with(mock_ctx)
    mock_delete_instance.assert_called_once_with(
        mock_box_client, "123456", "customer_template"
    )
    assert result == delete_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_create")
async def test_box_metadata_template_create_tool_empty_fields(
    mock_create, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_template_create_tool function with empty fields"""
    mock_get_client.return_value = mock_box_client
    empty_template_response = {"templateKey": "empty_template", "fields": []}
    mock_create.return_value = empty_template_response

    result = await box_metadata_template_create_tool(
        ctx=mock_ctx, display_name="Empty Template", fields=[]
    )

    mock_create.assert_called_once_with(
        mock_box_client, "Empty Template", [], template_key=None
    )
    assert result == empty_template_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_set_instance_on_file")
async def test_box_metadata_set_instance_on_file_tool_empty_metadata(
    mock_set_instance, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_set_instance_on_file_tool function with empty metadata"""
    mock_get_client.return_value = mock_box_client
    empty_metadata_response = {
        "$parent": "file_123456",
        "$template": "template_key",
        "extra_data": {},
    }
    mock_set_instance.return_value = empty_metadata_response

    result = await box_metadata_set_instance_on_file_tool(
        ctx=mock_ctx, template_key="template_key", file_id="123456", metadata={}
    )

    mock_set_instance.assert_called_once_with(
        mock_box_client, "template_key", "123456", {}
    )
    assert result == empty_metadata_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_get_by_key")
async def test_box_metadata_template_get_by_key_tool_not_found(
    mock_get_by_key, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_template_get_by_key_tool function with non-existent template"""
    mock_get_client.return_value = mock_box_client
    error_response = {"error": "Template not found - 404"}
    mock_get_by_key.return_value = error_response

    result = await box_metadata_template_get_by_key_tool(
        ctx=mock_ctx, template_name="non_existent_template"
    )

    mock_get_by_key.assert_called_once_with(mock_box_client, "non_existent_template")
    assert result == error_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_get_instance_on_file")
async def test_box_metadata_get_instance_on_file_tool_not_found(
    mock_get_instance, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_get_instance_on_file_tool function with non-existent metadata instance"""
    mock_get_client.return_value = mock_box_client
    error_response = {"error": "Metadata instance not found - 404"}
    mock_get_instance.return_value = error_response

    result = await box_metadata_get_instance_on_file_tool(
        ctx=mock_ctx, file_id="123456", template_key="non_existent_template"
    )

    mock_get_instance.assert_called_once_with(
        mock_box_client, "123456", "non_existent_template"
    )
    assert result == error_response


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_create")
async def test_box_metadata_template_create_tool_exception_handling(
    mock_create, mock_get_client, mock_ctx, mock_box_client, sample_template_fields
):
    """Test exception handling in box_metadata_template_create_tool"""
    mock_get_client.return_value = mock_box_client
    mock_create.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        await box_metadata_template_create_tool(
            ctx=mock_ctx, display_name="Test Template", fields=sample_template_fields
        )

    assert str(exc_info.value) == "API Error"


@pytest.mark.asyncio
@patch("tools.box_tools_metadata.get_box_client")
@patch("tools.box_tools_metadata.box_metadata_template_create")
async def test_box_metadata_template_create_tool_complex_fields(
    mock_create, mock_get_client, mock_ctx, mock_box_client
):
    """Test box_metadata_template_create_tool function with complex field types"""
    mock_get_client.return_value = mock_box_client

    complex_fields = [
        {
            "type": "multiSelect",
            "key": "role",
            "displayName": "Contact Role",
            "options": [
                {"key": "Developer"},
                {"key": "Business Owner"},
                {"key": "Marketing"},
                {"key": "Legal"},
                {"key": "Sales"},
            ],
        },
        {
            "type": "float",
            "key": "score",
            "displayName": "Customer Score",
            "description": "Rating from 0.0 to 10.0",
        },
    ]

    complex_template_response = {
        "templateKey": "complex_template",
        "displayName": "Complex Template",
        "fields": complex_fields,
    }
    mock_create.return_value = complex_template_response

    result = await box_metadata_template_create_tool(
        ctx=mock_ctx,
        display_name="Complex Template",
        fields=complex_fields,
        template_key="complex_template",
    )

    mock_create.assert_called_once_with(
        mock_box_client,
        "Complex Template",
        complex_fields,
        template_key="complex_template",
    )
    assert result == complex_template_response
