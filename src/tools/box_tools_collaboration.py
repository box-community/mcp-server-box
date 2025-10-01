from datetime import datetime

from box_ai_agents_toolkit import (
    box_collaboration_delete,
    box_collaboration_file_group_by_group_id,
    box_collaboration_file_user_by_user_id,
    box_collaboration_file_user_by_user_login,
    box_collaboration_folder_group_by_group_id,
    box_collaboration_folder_user_by_user_id,
    box_collaboration_folder_user_by_user_login,
    box_collaboration_update,
    box_collaborations_list_by_file,
    box_collaborations_list_by_folder,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_collaboration_list_by_file_tool(ctx: Context, file_id: str) -> dict:
    """List all collaborations on a specific file.
    Args:
        ctx (Context): The MCP context.
        file_id (str): The ID of the file to list collaborations for.
    Returns:
        dict: A dictionary containing the list of collaborations or an error message.
    """
    client = get_box_client(ctx)
    return box_collaborations_list_by_file(client, file_id)


async def box_collaboration_list_by_folder_tool(ctx: Context, folder_id: str) -> dict:
    """List all collaborations on a specific folder.
    Args:
        ctx (Context): The MCP context.
        folder_id (str): The ID of the folder to list collaborations for.
    Returns:
        dict: A dictionary containing the list of collaborations or an error message.
    """
    client = get_box_client(ctx)
    return box_collaborations_list_by_folder(client, folder_id)


async def box_collaboration_delete_tool(ctx: Context, collaboration_id: str) -> dict:
    """Delete a specific collaboration.
    Args:
        ctx (Context): The MCP context.
        collaboration_id (str): The ID of the collaboration to delete.
    Returns:
        dict: A dictionary containing the result of the deletion or an error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_delete(client, collaboration_id)


async def box_collaboration_file_group_by_group_id_tool(
    ctx: Context,
    file_id: str,
    group_id: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a file with a group specified by group ID.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        group_id (str): The ID of the group to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_file_group_by_group_id(
        client, file_id, group_id, role, is_access_only, expires_at, notify
    )


async def box_collaboration_file_user_by_user_id_tool(
    ctx: Context,
    file_id: str,
    user_id: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a file with a user specified by user ID.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        user_id (str): The ID of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_file_user_by_user_id(
        client, file_id, user_id, role, is_access_only, expires_at, notify
    )


async def box_collaboration_file_user_by_user_login_tool(
    ctx: Context,
    file_id: str,
    user_login: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a file with a user specified by user login (email).
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        user_login (str): The login (email) of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_file_user_by_user_login(
        client, file_id, user_login, role, is_access_only, expires_at, notify
    )


async def box_collaboration_folder_group_by_group_id_tool(
    ctx: Context,
    folder_id: str,
    group_id: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    can_view_path: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a folder with a group specified by group ID.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        group_id (str): The ID of the group to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_folder_group_by_group_id(
        client,
        folder_id,
        group_id,
        role,
        is_access_only,
        can_view_path,
        expires_at,
        notify,
    )


async def box_collaboration_folder_user_by_user_id_tool(
    ctx: Context,
    folder_id: str,
    user_id: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    can_view_path: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a folder with a user specified by user ID.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        user_id (str): The ID of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_folder_user_by_user_id(
        client,
        folder_id,
        user_id,
        role,
        is_access_only,
        can_view_path,
        expires_at,
        notify,
    )


async def box_collaboration_folder_user_by_user_login_tool(
    ctx: Context,
    folder_id: str,
    user_login: str,
    role: str = "editor",
    is_access_only: bool | None = None,
    can_view_path: bool | None = None,
    expires_at: datetime | None = None,
    notify: bool | None = None,
) -> dict:
    """Create a collaboration on a folder with a user specified by user login (email).
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        user_login (str): The login (email) of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_folder_user_by_user_login(
        client,
        folder_id,
        user_login,
        role,
        is_access_only,
        can_view_path,
        expires_at,
        notify,
    )


async def box_collaboration_update_tool(
    ctx: Context,
    collaboration_id: str,
    role: str = "editor",
    status: str | None = None,
    expires_at: datetime | None = None,
    can_view_path: bool | None = None,
) -> dict:
    """Update a specific collaboration's role.
    Args:
        ctx (Context): The MCP context.
        collaboration_id (str): The ID of the collaboration to update.
        role (str): The new role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        status (Optional[str]): The status of the collaboration. Can be 'accepted' or 'rejected'.
        expires_at (Optional[datetime]): The new expiration date of the collaboration.
        can_view_path (Optional[bool]): Whether the collaborator can view the path to the root folder.
    Returns:
        dict: A dictionary containing the updated collaboration details or an error message.
    """
    client = get_box_client(ctx)
    return box_collaboration_update(client, collaboration_id, role)
