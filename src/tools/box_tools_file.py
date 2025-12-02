import base64
from datetime import datetime
from typing import Any

from box_ai_agents_toolkit import (
    box_file_copy,
    box_file_delete,
    box_file_info,
    box_file_lock,
    box_file_move,
    box_file_rename,
    box_file_retention_date_clear,
    box_file_retention_date_set,
    box_file_set_description,
    box_file_set_download_company,
    box_file_set_download_open,
    box_file_set_download_reset,
    box_file_tag_add,
    box_file_tag_list,
    box_file_tag_remove,
    box_file_thumbnail_download,
    box_file_thumbnail_url,
    box_file_unlock,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_file_info_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Get information about a file in Box.
    Args:
        file_id (str): The ID of the file to get information about.
    return:
        dict[str, Any]: Information about the file.
    """
    box_client = get_box_client(ctx)
    return box_file_info(box_client, file_id)


async def box_file_copy_tool(
    ctx: Context,
    file_id: str,
    destination_folder_id: str,
    new_name: str | None = None,
    version_number: int | None = None,
) -> dict[str, Any]:
    """
    Copy a file to a specified destination folder in Box.
    Args:
        file_id (str): The ID of the file to copy.
        destination_folder_id (str): The ID of the destination folder.
        new_name (str, optional): Optional new name for the copied file.
        version_number (int, optional): Optional version number of the file to copy.
    Returns:
        dict[str, Any]: Dictionary containing the copied file information or error message.
    """
    box_client = get_box_client(ctx)
    return box_file_copy(
        box_client, file_id, destination_folder_id, new_name, version_number
    )


async def box_file_delete_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Delete a file from Box.
    Args:
        file_id (str): The ID of the file to delete.
    Returns:
        dict[str, Any]: Dictionary containing success message or error.
    """
    box_client = get_box_client(ctx)
    return box_file_delete(box_client, file_id)


async def box_file_move_tool(
    ctx: Context,
    file_id: str,
    destination_folder_id: str,
) -> dict[str, Any]:
    """
    Move a file to a specified destination folder in Box.
    Args:
        file_id (str): The ID of the file to move.
        destination_folder_id (str): The ID of the destination folder.
    Returns:
        dict[str, Any]: Dictionary containing the moved file information.
    """
    box_client = get_box_client(ctx)
    return box_file_move(box_client, file_id, destination_folder_id)


async def box_file_rename_tool(
    ctx: Context,
    file_id: str,
    new_name: str,
) -> dict[str, Any]:
    """
    Rename a file in Box.
    Args:
        file_id (str): The ID of the file to rename.
        new_name (str): The new name for the file.
    Returns:
        dict[str, Any]: Dictionary containing the renamed file information.
    """
    box_client = get_box_client(ctx)
    return box_file_rename(box_client, file_id, new_name)


async def box_file_set_description_tool(
    ctx: Context,
    file_id: str,
    description: str,
) -> dict[str, Any]:
    """
    Set or update the description of a file in Box.
    Args:
        file_id (str): The ID of the file to update.
        description (str): The new description for the file.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information.
    """
    box_client = get_box_client(ctx)
    return box_file_set_description(box_client, file_id, description)


async def box_file_retention_date_set_tool(
    ctx: Context,
    file_id: str,
    retention_date: str,
) -> dict[str, Any]:
    """
    Set a retention date for a file in Box (cannot be shortened once set).
    Args:
        file_id (str): The ID of the file to update.
        retention_date (str): The retention date for the file in ISO 8601 format.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information including retention date.
    """
    box_client = get_box_client(ctx)
    # Parse the retention date string to datetime
    retention_dt = datetime.fromisoformat(retention_date.replace("Z", "+00:00"))
    return box_file_retention_date_set(box_client, file_id, retention_dt)


async def box_file_retention_date_clear_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Clear/remove the retention date from a file in Box.
    Args:
        file_id (str): The ID of the file to update.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information.
    """
    box_client = get_box_client(ctx)
    return box_file_retention_date_clear(box_client, file_id)


async def box_file_lock_tool(
    ctx: Context,
    file_id: str,
    lock_expires_at: str | None = None,
    is_download_prevented: bool | None = None,
) -> dict[str, Any]:
    """
    Define a lock on a file to prevent it from being moved, renamed, or changed by anyone other than the lock creator.
    Args:
        file_id (str): The ID of the file to lock.
        lock_expires_at (str, optional): Optional expiration date/time for the lock in ISO 8601 format.
        is_download_prevented (bool, optional): Optional flag to prevent downloads while locked.
    Returns:
        dict[str, Any]: Dictionary containing the locked file information including lock details.
    """
    box_client = get_box_client(ctx)

    lock_expires_dt = None
    if lock_expires_at:
        lock_expires_dt = datetime.fromisoformat(lock_expires_at.replace("Z", "+00:00"))

    return box_file_lock(
        box_client, file_id, lock_expires_dt, is_download_prevented
    )


async def box_file_unlock_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Remove a lock from a file in Box.
    Args:
        file_id (str): The ID of the file to unlock.
    Returns:
        dict[str, Any]: Dictionary containing the unlocked file information.
    """
    box_client = get_box_client(ctx)
    return box_file_unlock(box_client, file_id)


async def box_file_set_download_open_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Allow anyone with access to the file to download it (overrides role-based download permissions).
    Args:
        file_id (str): The ID of the file to update.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information.
    """
    box_client = get_box_client(ctx)
    return box_file_set_download_open(box_client, file_id)


async def box_file_set_download_company_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Set a file to be downloadable by company users (restricts external user downloads for viewer/editor roles).
    Args:
        file_id (str): The ID of the file to update.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information.
    """
    box_client = get_box_client(ctx)
    return box_file_set_download_company(box_client, file_id)


async def box_file_set_download_reset_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Reset download permissions to default behavior based on collaboration roles.
    Args:
        file_id (str): The ID of the file to update.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information.
    """
    box_client = get_box_client(ctx)
    return box_file_set_download_reset(box_client, file_id)


async def box_file_tag_list_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    List all tags associated with a file in Box.
    Args:
        file_id (str): The ID of the file to retrieve tags for.
    Returns:
        dict[str, Any]: Dictionary with list of tags or message if no tags found.
    """
    box_client = get_box_client(ctx)
    return box_file_tag_list(box_client, file_id)


async def box_file_tag_add_tool(
    ctx: Context,
    file_id: str,
    tag: str,
) -> dict[str, Any]:
    """
    Add a tag to a file in Box (prevents duplicates).
    Args:
        file_id (str): The ID of the file to add a tag to.
        tag (str): The tag to add.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information including tags.
    """
    box_client = get_box_client(ctx)
    return box_file_tag_add(box_client, file_id, tag)


async def box_file_tag_remove_tool(
    ctx: Context,
    file_id: str,
    tag: str,
) -> dict[str, Any]:
    """
    Remove a tag from a file in Box.
    Args:
        file_id (str): The ID of the file to remove a tag from.
        tag (str): The tag to remove.
    Returns:
        dict[str, Any]: Dictionary containing the updated file information including tags.
    """
    box_client = get_box_client(ctx)
    return box_file_tag_remove(box_client, file_id, tag)


async def box_file_thumbnail_url_tool(
    ctx: Context,
    file_id: str,
    extension: str | None = None,
    min_height: int | None = None,
    min_width: int | None = None,
    max_height: int | None = None,
    max_width: int | None = None,
) -> dict[str, Any]:
    """
    Retrieve the URL for a thumbnail image of a file.
    Args:
        file_id (str): The ID of the file.
        extension (str, optional): Image format ('png' or 'jpg', defaults to 'png').
        min_height (int, optional): Minimum height in pixels (32-320).
        min_width (int, optional): Minimum width in pixels (32-320).
        max_height (int, optional): Maximum height in pixels (32-320).
        max_width (int, optional): Maximum width in pixels (32-320).
    Returns:
        dict[str, Any]: Dictionary with thumbnail URL or message if not available.
    """
    box_client = get_box_client(ctx)
    return box_file_thumbnail_url(
        box_client, file_id, extension, min_height, min_width, max_height, max_width
    )


async def box_file_thumbnail_download_tool(
    ctx: Context,
    file_id: str,
    extension: str | None = None,
    min_height: int | None = None,
    min_width: int | None = None,
    max_height: int | None = None,
    max_width: int | None = None,
) -> dict[str, Any]:
    """
    Download the actual thumbnail image of a file.
    Args:
        file_id (str): The ID of the file.
        extension (str, optional): Image format ('png' or 'jpg', defaults to 'png').
        min_height (int, optional): Minimum height in pixels (32-320).
        min_width (int, optional): Minimum width in pixels (32-320).
        max_height (int, optional): Maximum height in pixels (32-320).
        max_width (int, optional): Maximum width in pixels (32-320).
    Returns:
        dict[str, Any]: Dictionary with thumbnail image content in base64 or error message.
    """
    box_client = get_box_client(ctx)
    result = box_file_thumbnail_download(
        box_client, file_id, extension, min_height, min_width, max_height, max_width
    )

    # If the result contains binary data, encode it as base64
    if isinstance(result, dict) and "content" in result:
        if isinstance(result["content"], bytes):
            result["content"] = base64.b64encode(result["content"]).decode("utf-8")

    return result
