from datetime import datetime

from box_ai_agents_toolkit import (
    box_shared_link_file_create_or_update,
    box_shared_link_file_find_by_shared_link_url,
    box_shared_link_file_get,
    box_shared_link_file_remove,
    box_shared_link_folder_create_or_update,
    box_shared_link_folder_find_by_shared_link_url,
    box_shared_link_folder_get,
    box_shared_link_folder_remove,
    box_shared_link_web_link_create_or_update,
    box_shared_link_web_link_find_by_shared_link_url,
    box_shared_link_web_link_get,
    box_shared_link_web_link_remove,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_shared_link_file_get_tool(ctx: Context, file_id: str) -> dict:
    """
    Get a shared link for a file.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to get the shared link for.

    Returns:
        dict: The response from the Box API containing the shared link details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_file_get(box_client, file_id=file_id)


async def box_shared_link_file_create_or_update_tool(
    ctx: Context,
    file_id: str,
    access: str | None = "company",
    can_download: bool | None = True,
    can_preview: bool | None = True,
    can_edit: bool | None = False,
    password: str | None = None,
    vanity_name: str | None = None,
    unshared_at: datetime | None = None,
) -> dict:
    """
    Create or update a shared link for a file.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to create or update the shared link for.
        access (str, optional): The access level for the shared link. Defaults to None.
        unshared_at (str, optional): The expiration date for the shared link. Defaults to None.
        password (str, optional): The password for the shared link. Defaults to None.
        permissions (dict, optional): The permissions for the shared link. Defaults to None.

    Returns:
        dict: The response from the Box API after creating or updating the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_file_create_or_update(
        box_client,
        file_id=file_id,
        access=access,
        can_download=can_download,
        can_preview=can_preview,
        can_edit=can_edit,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
    )


async def box_shared_link_file_remove_tool(ctx: Context, file_id: str) -> dict:
    """
    Remove a shared link from a file.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to remove the shared link from.

    Returns:
        dict: The response from the Box API after removing the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_file_remove(box_client, file_id=file_id)


async def box_shared_link_file_find_by_shared_link_url_tool(
    ctx: Context, shared_link_url: str, password: str | None = None
) -> dict:
    """
    Find a file by its shared link URL.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        shared_link_url (str): The shared link URL of the file to find.
        password (str, optional): The password for the shared link, if applicable. Defaults to None.

    Returns:
        dict: The response from the Box API containing the file details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_file_find_by_shared_link_url(
        box_client, shared_link_url=shared_link_url, password=password
    )


async def box_shared_link_folder_get_tool(ctx: Context, folder_id: str) -> dict:
    """
    Get a shared link for a folder.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        folder_id (str): The ID of the folder to get the shared link for.
    Returns:
        dict: The response from the Box API containing the shared link details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_folder_get(box_client, folder_id=folder_id)


async def box_shared_link_folder_create_or_update_tool(
    ctx: Context,
    folder_id: str,
    access: str | None = "company",
    can_download: bool | None = True,
    can_preview: bool | None = True,
    can_edit: bool | None = False,
    password: str | None = None,
    vanity_name: str | None = None,
    unshared_at: datetime | None = None,
) -> dict:
    """
    Create or update a shared link for a folder.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        folder_id (str): The ID of the folder to create or update the shared link for.
        access (str, optional): The access level for the shared link. Defaults to None.
        unshared_at (str, optional): The expiration date for the shared link. Defaults to None.
        password (str, optional): The password for the shared link. Defaults to None.
        permissions (dict, optional): The permissions for the shared link. Defaults to None.

    Returns:
        dict: The response from the Box API after creating or updating the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_folder_create_or_update(
        box_client,
        folder_id=folder_id,
        access=access,
        can_download=can_download,
        can_preview=can_preview,
        can_edit=can_edit,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
    )


async def box_shared_link_folder_remove_tool(ctx: Context, folder_id: str) -> dict:
    """
    Remove a shared link from a folder.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        folder_id (str): The ID of the folder to remove the shared link from.

    Returns:
        dict: The response from the Box API after removing the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_folder_remove(box_client, folder_id=folder_id)


async def box_shared_link_folder_find_by_shared_link_url_tool(
    ctx: Context, shared_link_url: str, password: str | None = None
) -> dict:
    """
    Find a folder by its shared link URL.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        shared_link_url (str): The shared link URL of the folder to find.
        password (str, optional): The password for the shared link, if applicable. Defaults to None.

    Returns:
        dict: The response from the Box API containing the folder details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_folder_find_by_shared_link_url(
        box_client, shared_link_url=shared_link_url, password=password
    )


async def box_shared_link_web_link_create_or_update_tool(
    ctx: Context,
    web_link_id: str,
    access: str | None = "company",
    password: str | None = None,
    vanity_name: str | None = None,
    unshared_at: datetime | None = None,
) -> dict:
    """
    Create or update a shared link for a web link.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to create or update the shared link for.
        access (str, optional): The access level for the shared link. Defaults to None.
        unshared_at (str, optional): The expiration date for the shared link. Defaults to None.
        password (str, optional): The password for the shared link. Defaults to None.
        vanity_name (str, optional): The vanity name for the shared link. Defaults to None

    Returns:
        dict: The response from the Box API after creating or updating the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_web_link_create_or_update(
        box_client,
        web_link_id=web_link_id,
        access=access,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
    )


async def box_shared_link_web_link_get_tool(ctx: Context, web_link_id: str) -> dict:
    """
    Get a shared link for a web link.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to get the shared link for.
    Returns:
        dict: The response from the Box API containing the shared link details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_web_link_get(box_client, web_link_id=web_link_id)


async def box_shared_link_web_link_remove_tool(ctx: Context, web_link_id: str) -> dict:
    """
    Remove a shared link from a web link.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to remove the shared link from.

    Returns:
        dict: The response from the Box API after removing the shared link.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_web_link_remove(box_client, web_link_id=web_link_id)


async def box_shared_link_web_link_find_by_shared_link_url_tool(
    ctx: Context, shared_link_url: str, password: str | None = None
) -> dict:
    """
    Find a web link by its shared link URL.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        shared_link_url (str): The shared link URL of the web link to find.
        password (str, optional): The password for the shared link, if applicable. Defaults to None.

    Returns:
        dict: The response from the Box API containing the web link details.
    """
    box_client = get_box_client(ctx)
    return box_shared_link_web_link_find_by_shared_link_url(
        box_client, shared_link_url=shared_link_url, password=password
    )
