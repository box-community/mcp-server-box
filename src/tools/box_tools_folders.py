from typing import Optional

from box_ai_agents_toolkit import (
    box_folder_copy,
    box_folder_create,
    box_folder_delete,
    box_folder_favorites_add,
    box_folder_favorites_remove,
    box_folder_info,
    box_folder_items_list,
    box_folder_list_tags,
    box_folder_move,
    box_folder_rename,
    box_folder_set_collaboration,
    box_folder_set_description,
    box_folder_set_sync,
    box_folder_set_upload_email,
    box_folder_tag_add,
    box_folder_tag_remove,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_folder_copy_tool(
    ctx: Context,
    folder_id: str,
    destination_parent_folder_id: str,
    name: Optional[str] = None,
) -> dict:
    """
    Copies a folder to a new location in Box.

    Args:
        ctx: Context: The context containing Box client information
        folder_id (str): ID of the folder to copy. Can be string or int.
        destination_parent_folder_id (str): ID of the destination parent folder. Can be string or int.
        name (str, optional): New name for the copied folder. If not provided, original name is used.
    Returns:
        dict[str, Any]: Dictionary containing the copied folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_copy(
        client=client,
        folder_id=folder_id,
        destination_parent_folder_id=destination_parent_folder_id,
        name=name,
    )


async def box_folder_create_tool(
    ctx: Context,
    name: str,
    parent_folder_id: str = "0",
) -> dict:
    """
    Creates a new folder in Box.
    Args:
        ctx: Context: The context containing Box client information
        name (str): Name of the new folder
        parent_folder_id (str): ID of the parent folder where the new folder will be created, use "0" for root folder
    Returns:
        dict[str, Any]: Dictionary containing the created folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_create(
        client=client,
        name=name,
        parent_folder_id=parent_folder_id,
    )


async def box_folder_delete_tool(
    ctx: Context,
    folder_id: str,
    recursive: bool = False,
) -> dict:
    """
    Deletes a folder from Box.

    Args:
        ctx: Context: The context containing Box client information
        folder_id (str): ID of the folder to delete. Can be string or int.
        recursive (bool, optional): Whether to delete recursively. Defaults to False.
    Returns:
        dict[str, Any]: Dictionary containing success message or error message
    """
    client = get_box_client(ctx)
    return box_folder_delete(
        client=client,
        folder_id=folder_id,
        recursive=recursive,
    )


async def box_folder_favorites_add_tool(
    ctx: Context,
    folder_id: str,
) -> dict:
    """
    Adds a folder to the user's favorites in Box.

    Args:
        ctx: Context: The context containing Box client information
        folder_id (str): ID of the folder to add to favorites.

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_favorites_add(
        client=client,
        folder_id=folder_id,
    )


async def box_folder_favorites_remove_tool(
    ctx: Context,
    folder_id: str,
) -> dict:
    """
    Removes a folder from the user's favorites in Box.

    Args:
        ctx: Context: The context containing Box client information
        folder_id (str): ID of the folder to remove from favorites.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_favorites_remove(
        client=client,
        folder_id=folder_id,
    )


async def box_folder_info_tool(
    ctx: Context,
    folder_id: str,
) -> dict:
    """
    Retrieve information about a specific folder in Box.

    Args:
        ctx: Context: The context containing Box client information
        folder_id (str): ID of the folder to retrieve information for.
    Returns:
        dict[str, Any]: Dictionary containing folder information or error message.
    """
    client = get_box_client(ctx)
    return box_folder_info(
        client=client,
        folder_id=folder_id,
    )


async def box_folder_items_list_tool(
    ctx: Context,
    folder_id: str,
    is_recursive: bool = False,
    limit: Optional[int] = 1000,
) -> dict:
    """
    List items in a Box folder with optional recursive traversal.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to list items from.
        is_recursive (bool, optional): Whether to recursively list subfolder contents. Defaults to False.
        limit (Optional[int], optional): Maximum items per API call. Defaults to 1000.

    Returns:
        dict[str, Any]: Dictionary containing folder items list or error message.
    """
    client = get_box_client(ctx)
    return box_folder_items_list(
        client=client,
        folder_id=folder_id,
        is_recursive=is_recursive,
        limit=limit,
    )


async def box_folder_list_tags_tool(
    ctx: Context,
    folder_id: str,
) -> dict:
    """
    Lists tags associated with a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to list tags for.

    Returns:
        dict[str, Any]: Dictionary containing the list of tags or error message
    """
    client = get_box_client(ctx)
    return box_folder_list_tags(
        client=client,
        folder_id=folder_id,
    )


async def box_folder_move_tool(
    ctx: Context,
    folder_id: str,
    destination_parent_folder_id: str,
) -> dict:
    """
    Moves a folder to a new location in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to move.
        destination_parent_folder_id (str): ID of the destination parent folder.
    Returns:
        dict[str, Any]: Dictionary containing the moved folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_move(
        client=client,
        folder_id=folder_id,
        destination_parent_folder_id=destination_parent_folder_id,
    )


async def box_folder_rename_tool(
    ctx: Context,
    folder_id: str,
    new_name: str,
) -> dict:
    """
    Renames a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to rename.
        new_name (str): New name for the folder.
    Returns:
        dict[str, Any]: Dictionary containing the renamed folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_rename(
        client=client,
        folder_id=folder_id,
        new_name=new_name,
    )


async def box_folder_set_collaboration_tool(
    ctx: Context,
    folder_id: str,
    can_non_owners_invite: bool,
    can_non_owners_view_collaborators: bool,
    is_collaboration_restricted_to_enterprise: bool,
) -> dict:
    """
    Sets collaboration settings for a folder in Box.
    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to set collaboration settings for.
        can_non_owners_invite (bool): Specifies if users who are not the owner of the folder can invite new collaborators to the folder.
        can_non_owners_view_collaborators (bool): Restricts collaborators who are not the owner of this folder from viewing other collaborations on this folder.
        is_collaboration_restricted_to_enterprise (bool): Specifies if new invites to this folder are restricted to users within the enterprise. This does not affect existing collaborations.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_set_collaboration(
        client=client,
        folder_id=folder_id,
        can_non_owners_invite=can_non_owners_invite,
        can_non_owners_view_collaborators=can_non_owners_view_collaborators,
        is_collaboration_restricted_to_enterprise=is_collaboration_restricted_to_enterprise,
    )


async def box_folder_set_description_tool(
    ctx: Context,
    folder_id: str,
    description: str,
) -> dict:
    """
    Sets the description of a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to set description for.
        description (str): Description text to set for the folder.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_set_description(
        client=client,
        folder_id=folder_id,
        description=description,
    )


async def box_folder_set_sync_tool(
    ctx: Context,
    folder_id: str,
    sync_state: str,
) -> dict:
    """
    Sets the sync state for a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to set sync state for.
        sync_state (str): Specifies whether a folder should be synced to a user's device or not. This is used by Box Sync (discontinued) and is not used by Box Drive. Value is one of synced,not_synced,partially_synced

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_set_sync(
        client=client,
        folder_id=folder_id,
        sync_state=sync_state,
    )


async def box_folder_set_upload_email_tool(
    ctx: Context,
    folder_id: str,
    folder_upload_email_access: Optional[str] = "collaborators",
) -> dict:
    """
    Sets or removes the upload email address for a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to set the upload email for.
        folder_upload_email_access (Optional[str]): The upload email access level to set. If None, removes the upload email.
                                            When set to open it will accept emails from any email address.
                                            Value is one of open,collaborators

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_set_upload_email(
        client=client,
        folder_id=folder_id,
        folder_upload_email_access=folder_upload_email_access,
    )


async def box_folder_tag_add_tool(
    ctx: Context,
    folder_id: str,
    tag: str,
) -> dict:
    """
    Adds a tag to a folder in Box.

    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to add tag to.
        tag (str): Tag to add to the folder.

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_tag_add(
        client=client,
        folder_id=folder_id,
        tag=tag,
    )


async def box_folder_tag_remove_tool(
    ctx: Context,
    folder_id: str,
    tag: str,
) -> dict:
    """
    Removes a tag from a folder in Box.
    Args:
        ctx: Context: The context containing Box client information.
        folder_id (str): ID of the folder to remove tag from.
        tag (str): Tag to remove from the folder.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    client = get_box_client(ctx)
    return box_folder_tag_remove(
        client=client,
        folder_id=folder_id,
        tag=tag,
    )
