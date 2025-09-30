from typing import Any, Optional

from box_ai_agents_toolkit import (
    box_docgen_create_batch,
    box_docgen_create_single_file_from_user_input,
    box_docgen_get_job_by_id,
    box_docgen_list_jobs,
    box_docgen_list_jobs_by_batch,
    box_docgen_template_create,
    box_docgen_template_delete,
    box_docgen_template_get_by_id,
    box_docgen_template_get_by_name,
    box_docgen_template_list,
    box_docgen_template_list_jobs,
    box_docgen_template_list_tags,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client

# region DocGen Templates


async def box_docgen_template_create_tool(ctx: Context, file_id: str) -> dict[str, Any]:
    """
    Mark a file as a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to mark as template.

    Returns:
        dict[str, Any]: Metadata of the created template.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_create(box_client, file_id)


async def box_docgen_template_list_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """
    List all Box Doc Gen templates accessible to the user.

    Args:
        client (BoxClient): Authenticated Box client.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        dict[str, Any] | list[dict[str, Any]]: A list of template metadata or an error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_list(box_client, marker=marker, limit=limit)


async def box_docgen_template_get_by_id_tool(
    ctx: Context, template_id: str
) -> dict[str, Any]:
    """
    Retrieve details of a specific Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.

    Returns:
        dict[str, Any]: Metadata of the template or an error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_get_by_id(box_client, template_id)


async def box_docgen_template_get_by_name_tool(
    ctx: Context, template_name: str
) -> dict[str, Any]:
    """
    Retrieve details of a specific Box Doc Gen template by name.

    Args:
        client (BoxClient): Authenticated Box client.
        template_name (str): Name of the template.

    Returns:
        dict[str, Any]: Metadata of the template or an error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_get_by_name(box_client, template_name)


async def box_docgen_template_delete_tool(
    ctx: Context, template_id: str
) -> dict[str, Any]:
    """
    Un mark a file as a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template to delete.
    Returns:
        dict[str, Any]: Success message or an error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_delete(box_client, template_id)


async def box_docgen_template_list_tags_tool(
    ctx: Context,
    template_id: str,
    template_version_id: str | None = None,
    marker: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """
    List all tags for a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.
        template_version_id (str, optional): Specific version ID.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        list[dict[str, Any]]: A list of tags for the template or an error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_list_tags(
        box_client,
        template_id,
        template_version_id=template_version_id,
        marker=marker,
        limit=limit,
    )


async def box_docgen_template_list_jobs_tool(
    ctx: Context,
    template_id: str,
    marker: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """
    List Doc Gen jobs that used a specific template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        DocGenJobsV2025R0: A page of Doc Gen jobs for the template.
    """
    box_client = get_box_client(ctx)
    return box_docgen_template_list_jobs(
        box_client, template_id=template_id, marker=marker, limit=limit
    )


# endregion DocGen Templates

# region DocGen Batches and Jobs


async def box_docgen_create_batch_tool(
    ctx: Context,
    docgen_template_id: str,
    destination_folder_id: str,
    document_generation_data: list[dict[str, Any]],
    output_type: str = "pdf",
) -> dict[str, Any]:
    """
    Create a new Box Doc Gen batch to generate documents from a template.

    Args:
        client (BoxClient): Authenticated Box client.
        docgen_template_id (str): ID of the Doc Gen template.
        destination_folder_id (str): ID of the folder to save the generated document.
        document_generation_data (List[Dict[str, Any]]): Data for document generation.
        example:
            [
                {
                    "generated_file_name": "Image test",
                    "user_input": {
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
                                    "amount": 2900
                                },
                            ]
                        }
                    }
                },
            ]
        output_type (str): Output file type (only, "pdf" or "docx").

    Returns:
        dict[str, Any]: Response containing batch creation status and details.
        If successful, contains a message with batch ID.
        If an error occurs, contains an "error" key with the error message.
    """
    box_client = get_box_client(ctx)
    return box_docgen_create_batch(
        box_client,
        docgen_template_id=docgen_template_id,
        destination_folder_id=destination_folder_id,
        document_generation_data=document_generation_data,
        output_type=output_type,
    )


async def box_docgen_create_single_file_from_user_input_tool(
    ctx: Context,
    docgen_template_id: str,
    destination_folder_id: str,
    user_input: dict[str, Any],
    generated_file_name: Optional[str] = None,
    output_type: str = "pdf",
) -> dict[str, Any]:
    """
    Create a single document from a Doc Gen template using user input.

    Args:
        client (BoxClient): Authenticated Box client.
        docgen_template_id (str): ID of the Doc Gen template.
        destination_folder_id (str): ID of the folder to save the generated document.
        user_input (dict[str, Any]): User input data for document generation.
        example:
        example:
            {
                "user_input": {
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
                                "amount": 2900
                            },
                        ]
                    }
                }
            }
        generated_file_name (Optional[str]): Name for the generated document file.
        output_type (str): Output file type (only, "pdf" or "docx").

    Returns:
        dict[str, Any]: Information about the created batch job.
    """
    box_client = get_box_client(ctx)
    return box_docgen_create_single_file_from_user_input(
        box_client,
        docgen_template_id=docgen_template_id,
        destination_folder_id=destination_folder_id,
        user_input=user_input,
        generated_file_name=generated_file_name,
        output_type=output_type,
    )


async def box_docgen_list_jobs_by_batch_tool(
    ctx: Context,
    batch_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """
    List Doc Gen jobs in a specific batch.

    Args:
        client (BoxClient): Authenticated Box client.
        batch_id (str): ID of the Doc Gen batch.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        list[dict[str, Any]]: A list of Doc Gen jobs in the batch.
    """
    box_client = get_box_client(ctx)
    return box_docgen_list_jobs_by_batch(
        box_client, batch_id=batch_id, marker=marker, limit=limit
    )


async def box_docgen_get_job_by_id_tool(ctx: Context, job_id: str) -> dict[str, Any]:
    """
    Retrieve a Box Doc Gen job by its ID.

    Args:
        client (BoxClient): Authenticated Box client.
        job_id (str): ID of the Doc Gen job.

    Returns:
        dict[str, Any]: Details of the specified Doc Gen job.
    """
    box_client = get_box_client(ctx)
    return box_docgen_get_job_by_id(box_client, job_id)


async def box_docgen_list_jobs_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """
    List all Box Doc Gen jobs for the current user.

    Args:
        client (BoxClient): Authenticated Box client.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        list[dict[str, Any]]: A list of Doc Gen jobs.
    """
    box_client = get_box_client(ctx)
    return box_docgen_list_jobs(box_client, marker=marker, limit=limit)


# endregion DocGen Batches and Jobs
