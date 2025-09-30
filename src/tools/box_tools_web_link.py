from box_ai_agents_toolkit import (
    box_web_link_create,
    box_web_link_get_by_id,
    box_web_link_update_by_id,
    box_web_link_delete_by_id,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_web_link_create_tool(
    ctx: Context,
    url: str,
    parent_folder_id: str,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    """
    Create a Box web link.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        url (str): The URL of the web link.
        parent_folder_id (str): The ID of the parent folder for the web link.
        name (str, optional): The name of the web link. Defaults to None.
        description (str, optional): The description of the web link. Defaults to None.

    Returns:
        dict: The response from the Box API after creating the web link.
    """
    box_client = get_box_client(ctx)
    return box_web_link_create(
        box_client,
        url=url,
        parent_folder_id=parent_folder_id,
        name=name,
        description=description,
    )


async def box_web_link_get_by_id_tool(ctx: Context, web_link_id: str) -> dict:
    """
    Get a Box web link by its ID.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to retrieve.

    Returns:
        dict: The response from the Box API containing the web link details.
    """
    box_client = get_box_client(ctx)
    return box_web_link_get_by_id(box_client, web_link_id=web_link_id)


async def box_web_link_update_by_id_tool(
    ctx: Context,
    web_link_id: str,
    url: str,
    parent_folder_id: str,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    """
    Update a Box web link by its ID.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to update.
        url (str): The new URL of the web link.
        parent_folder_id (str): The ID of the parent folder for the web link.
        name (str, optional): The new name of the web link. Defaults to None.
        description (str, optional): The new description of the web link. Defaults to None.

    Returns:
        dict: The response from the Box API after updating the web link.
    """
    box_client = get_box_client(ctx)
    return box_web_link_update_by_id(
        box_client,
        web_link_id=web_link_id,
        url=url,
        parent_folder_id=parent_folder_id,
        name=name,
        description=description,
    )


async def box_web_link_delete_by_id_tool(ctx: Context, web_link_id: str) -> dict:
    """
    Delete a Box web link by its ID.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        web_link_id (str): The ID of the web link to delete.

    Returns:
        dict: The response from the Box API after deleting the web link.
    """
    box_client = get_box_client(ctx)
    return box_web_link_delete_by_id(box_client, web_link_id=web_link_id)
