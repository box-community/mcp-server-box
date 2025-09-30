from unittest.mock import Mock, patch

import pytest

from tools.box_tools_docgen import (
    box_docgen_create_batch_tool,
    box_docgen_create_single_file_from_user_input_tool,
    box_docgen_get_job_by_id_tool,
    box_docgen_list_jobs_by_batch_tool,
    box_docgen_list_jobs_tool,
    box_docgen_template_create_tool,
    box_docgen_template_delete_tool,
    box_docgen_template_get_by_id_tool,
    box_docgen_template_get_by_name_tool,
    box_docgen_template_list_jobs_tool,
    box_docgen_template_list_tags_tool,
    box_docgen_template_list_tool,
)


@pytest.fixture
def sample_template_data():
    """Sample template data for testing."""
    return {
        "type": "doc_gen_template",
        "id": "template_123",
        "name": "Test Template",
        "file": {"type": "file", "id": "file_123", "name": "template.docx"},
    }


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "type": "doc_gen_job",
        "id": "job_123",
        "status": "completed",
        "generated_file": {
            "type": "file",
            "id": "generated_file_123",
            "name": "generated_document.pdf",
        },
    }


@pytest.fixture
def sample_batch_data():
    """Sample batch data for testing."""
    return {
        "type": "doc_gen_batch",
        "id": "batch_123",
        "status": "processing",
        "jobs": [{"type": "doc_gen_job", "id": "job_123", "status": "completed"}],
    }


@pytest.fixture
def sample_user_input():
    """Sample user input data for document generation."""
    return {
        "order": {
            "id": "12305",
            "date": "18-08-2023",
            "products": [
                {
                    "id": 1,
                    "name": "A4 Papers",
                    "type": "non-fragile",
                    "quantity": 100,
                    "price": 29,
                    "amount": 2900,
                }
            ],
        }
    }


@pytest.fixture
def sample_document_generation_data(sample_user_input):
    """Sample document generation data for batch processing."""
    return [{"generated_file_name": "Test Document", "user_input": sample_user_input}]


# DocGen Templates Tests


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_create")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_create_tool(
    mock_get_client, mock_create, ctx, sample_template_data
):
    """Test creating a DocGen template."""
    mock_get_client.return_value = Mock()
    mock_create.return_value = sample_template_data

    result = await box_docgen_template_create_tool(ctx, "file_123")

    assert result == sample_template_data
    mock_get_client.assert_called_once_with(ctx)
    mock_create.assert_called_once_with(mock_get_client.return_value, "file_123")


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_list")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_list_tool(mock_get_client, mock_list, ctx):
    """Test listing DocGen templates."""
    mock_get_client.return_value = Mock()
    mock_list.return_value = [{"id": "template_1"}, {"id": "template_2"}]

    result = await box_docgen_template_list_tool(ctx)

    assert len(result) == 2
    mock_get_client.assert_called_once_with(ctx)
    mock_list.assert_called_once_with(
        mock_get_client.return_value, marker=None, limit=None
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_list")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_list_tool_with_pagination(
    mock_get_client, mock_list, ctx
):
    """Test listing DocGen templates with pagination parameters."""
    mock_get_client.return_value = Mock()
    mock_list.return_value = [{"id": "template_1"}]

    result = await box_docgen_template_list_tool(ctx, marker="marker_123", limit=10)

    assert len(result) == 1
    mock_list.assert_called_once_with(
        mock_get_client.return_value, marker="marker_123", limit=10
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_get_by_id")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_get_by_id_tool(
    mock_get_client, mock_get_by_id, ctx, sample_template_data
):
    """Test getting a DocGen template by ID."""
    mock_get_client.return_value = Mock()
    mock_get_by_id.return_value = sample_template_data

    result = await box_docgen_template_get_by_id_tool(ctx, "template_123")

    assert result == sample_template_data
    mock_get_client.assert_called_once_with(ctx)
    mock_get_by_id.assert_called_once_with(mock_get_client.return_value, "template_123")


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_get_by_name")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_get_by_name_tool(
    mock_get_client, mock_get_by_name, ctx, sample_template_data
):
    """Test getting a DocGen template by name."""
    mock_get_client.return_value = Mock()
    mock_get_by_name.return_value = sample_template_data

    result = await box_docgen_template_get_by_name_tool(ctx, "Test Template")

    assert result == sample_template_data
    mock_get_client.assert_called_once_with(ctx)
    mock_get_by_name.assert_called_once_with(
        mock_get_client.return_value, "Test Template"
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_delete")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_delete_tool(mock_get_client, mock_delete, ctx):
    """Test deleting a DocGen template."""
    mock_get_client.return_value = Mock()
    mock_delete.return_value = {"message": "Template deleted successfully"}

    result = await box_docgen_template_delete_tool(ctx, "template_123")

    assert result["message"] == "Template deleted successfully"
    mock_get_client.assert_called_once_with(ctx)
    mock_delete.assert_called_once_with(mock_get_client.return_value, "template_123")


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_list_tags")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_list_tags_tool(mock_get_client, mock_list_tags, ctx):
    """Test listing tags for a DocGen template."""
    mock_get_client.return_value = Mock()
    mock_list_tags.return_value = [{"key": "tag1", "value": "value1"}]

    result = await box_docgen_template_list_tags_tool(ctx, "template_123")

    assert len(result) == 1
    assert result[0]["key"] == "tag1"
    mock_get_client.assert_called_once_with(ctx)
    mock_list_tags.assert_called_once_with(
        mock_get_client.return_value,
        "template_123",
        template_version_id=None,
        marker=None,
        limit=None,
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_list_tags")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_list_tags_tool_with_params(
    mock_get_client, mock_list_tags, ctx
):
    """Test listing tags for a DocGen template with all parameters."""
    mock_get_client.return_value = Mock()
    mock_list_tags.return_value = [{"key": "tag1", "value": "value1"}]

    result = await box_docgen_template_list_tags_tool(
        ctx, "template_123", template_version_id="v1", marker="marker_123", limit=5
    )

    assert len(result) == 1
    mock_list_tags.assert_called_once_with(
        mock_get_client.return_value,
        "template_123",
        template_version_id="v1",
        marker="marker_123",
        limit=5,
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_list_jobs")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_list_jobs_tool(mock_get_client, mock_list_jobs, ctx):
    """Test listing jobs for a DocGen template."""
    mock_get_client.return_value = Mock()
    mock_list_jobs.return_value = [{"id": "job_1"}, {"id": "job_2"}]

    result = await box_docgen_template_list_jobs_tool(ctx, "template_123")

    assert len(result) == 2
    mock_get_client.assert_called_once_with(ctx)
    mock_list_jobs.assert_called_once_with(
        mock_get_client.return_value,
        template_id="template_123",
        marker=None,
        limit=None,
    )


# DocGen Batches and Jobs Tests


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_create_batch")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_create_batch_tool(
    mock_get_client, mock_create_batch, ctx, sample_document_generation_data
):
    """Test creating a DocGen batch."""
    mock_get_client.return_value = Mock()
    mock_create_batch.return_value = {"batch_id": "batch_123", "status": "processing"}

    result = await box_docgen_create_batch_tool(
        ctx,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        document_generation_data=sample_document_generation_data,
    )

    assert result["batch_id"] == "batch_123"
    mock_get_client.assert_called_once_with(ctx)
    mock_create_batch.assert_called_once_with(
        mock_get_client.return_value,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        document_generation_data=sample_document_generation_data,
        output_type="pdf",
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_create_batch")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_create_batch_tool_with_docx_output(
    mock_get_client, mock_create_batch, ctx, sample_document_generation_data
):
    """Test creating a DocGen batch with DOCX output."""
    mock_get_client.return_value = Mock()
    mock_create_batch.return_value = {"batch_id": "batch_123", "status": "processing"}

    result = await box_docgen_create_batch_tool(
        ctx,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        document_generation_data=sample_document_generation_data,
        output_type="docx",
    )

    assert result["batch_id"] == "batch_123"
    mock_create_batch.assert_called_once_with(
        mock_get_client.return_value,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        document_generation_data=sample_document_generation_data,
        output_type="docx",
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_create_single_file_from_user_input")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_create_single_file_from_user_input_tool(
    mock_get_client, mock_create_single, ctx, sample_user_input
):
    """Test creating a single document from user input."""
    mock_get_client.return_value = Mock()
    mock_create_single.return_value = {"job_id": "job_123", "status": "processing"}

    result = await box_docgen_create_single_file_from_user_input_tool(
        ctx,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        user_input=sample_user_input,
    )

    assert result["job_id"] == "job_123"
    mock_get_client.assert_called_once_with(ctx)
    mock_create_single.assert_called_once_with(
        mock_get_client.return_value,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        user_input=sample_user_input,
        generated_file_name=None,
        output_type="pdf",
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_create_single_file_from_user_input")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_create_single_file_from_user_input_tool_with_name(
    mock_get_client, mock_create_single, ctx, sample_user_input
):
    """Test creating a single document from user input with custom filename."""
    mock_get_client.return_value = Mock()
    mock_create_single.return_value = {"job_id": "job_123", "status": "processing"}

    result = await box_docgen_create_single_file_from_user_input_tool(
        ctx,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        user_input=sample_user_input,
        generated_file_name="Custom Document Name",
        output_type="docx",
    )

    assert result["job_id"] == "job_123"
    mock_create_single.assert_called_once_with(
        mock_get_client.return_value,
        docgen_template_id="template_123",
        destination_folder_id="folder_123",
        user_input=sample_user_input,
        generated_file_name="Custom Document Name",
        output_type="docx",
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_list_jobs_by_batch")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_list_jobs_by_batch_tool(mock_get_client, mock_list_jobs, ctx):
    """Test listing jobs in a batch."""
    mock_get_client.return_value = Mock()
    mock_list_jobs.return_value = [{"id": "job_1"}, {"id": "job_2"}]

    result = await box_docgen_list_jobs_by_batch_tool(ctx, "batch_123")

    assert len(result) == 2
    mock_get_client.assert_called_once_with(ctx)
    mock_list_jobs.assert_called_once_with(
        mock_get_client.return_value, batch_id="batch_123", marker=None, limit=None
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_list_jobs_by_batch")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_list_jobs_by_batch_tool_with_pagination(
    mock_get_client, mock_list_jobs, ctx
):
    """Test listing jobs in a batch with pagination."""
    mock_get_client.return_value = Mock()
    mock_list_jobs.return_value = [{"id": "job_1"}]

    result = await box_docgen_list_jobs_by_batch_tool(
        ctx, "batch_123", marker="marker_123", limit=10
    )

    assert len(result) == 1
    mock_list_jobs.assert_called_once_with(
        mock_get_client.return_value,
        batch_id="batch_123",
        marker="marker_123",
        limit=10,
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_get_job_by_id")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_get_job_by_id_tool(
    mock_get_client, mock_get_job, ctx, sample_job_data
):
    """Test getting a job by ID."""
    mock_get_client.return_value = Mock()
    mock_get_job.return_value = sample_job_data

    result = await box_docgen_get_job_by_id_tool(ctx, "job_123")

    assert result == sample_job_data
    mock_get_client.assert_called_once_with(ctx)
    mock_get_job.assert_called_once_with(mock_get_client.return_value, "job_123")


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_list_jobs")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_list_jobs_tool(mock_get_client, mock_list_jobs, ctx):
    """Test listing all jobs for the current user."""
    mock_get_client.return_value = Mock()
    mock_list_jobs.return_value = [{"id": "job_1"}, {"id": "job_2"}]

    result = await box_docgen_list_jobs_tool(ctx)

    assert len(result) == 2
    mock_get_client.assert_called_once_with(ctx)
    mock_list_jobs.assert_called_once_with(
        mock_get_client.return_value, marker=None, limit=None
    )


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_list_jobs")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_list_jobs_tool_with_pagination(
    mock_get_client, mock_list_jobs, ctx
):
    """Test listing all jobs with pagination parameters."""
    mock_get_client.return_value = Mock()
    mock_list_jobs.return_value = [{"id": "job_1"}]

    result = await box_docgen_list_jobs_tool(ctx, marker="marker_123", limit=5)

    assert len(result) == 1
    mock_list_jobs.assert_called_once_with(
        mock_get_client.return_value, marker="marker_123", limit=5
    )


# Error handling tests


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_template_get_by_id")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_template_get_by_id_tool_error(
    mock_get_client, mock_get_by_id, ctx
):
    """Test handling errors when getting a template by ID."""
    mock_get_client.return_value = Mock()
    mock_get_by_id.return_value = {"error": "Template not found"}

    result = await box_docgen_template_get_by_id_tool(ctx, "nonexistent_template")

    assert "error" in result
    assert result["error"] == "Template not found"


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_create_batch")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_create_batch_tool_error(
    mock_get_client, mock_create_batch, ctx, sample_document_generation_data
):
    """Test handling errors when creating a batch."""
    mock_get_client.return_value = Mock()
    mock_create_batch.return_value = {"error": "Invalid template ID"}

    result = await box_docgen_create_batch_tool(
        ctx,
        docgen_template_id="invalid_template",
        destination_folder_id="folder_123",
        document_generation_data=sample_document_generation_data,
    )

    assert "error" in result
    assert result["error"] == "Invalid template ID"


@pytest.mark.asyncio
@patch("tools.box_tools_docgen.box_docgen_get_job_by_id")
@patch("tools.box_tools_docgen.get_box_client")
async def test_box_docgen_get_job_by_id_tool_error(mock_get_client, mock_get_job, ctx):
    """Test handling errors when getting a job by ID."""
    mock_get_client.return_value = Mock()
    mock_get_job.return_value = {"error": "Job not found"}

    result = await box_docgen_get_job_by_id_tool(ctx, "nonexistent_job")

    assert "error" in result
    assert result["error"] == "Job not found"
