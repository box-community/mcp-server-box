from box_ai_agents_toolkit import (
    box_groups_search,
    box_groups_list_members,
    box_groups_list_by_user,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_groups_search_tool(ctx: Context, query: str) -> dict:
    """Search for groups by name. This is a partial match search.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        query (str): The search query to match against group names.
    Returns:
        dict: A dictionary containing the list of matching groups."""
    client = get_box_client(ctx)
    return box_groups_search(client, query)


async def box_groups_list_members_tool(ctx: Context, group_id: str) -> dict:
    """List all members of a specific group.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        group_id (str): The ID of the group whose members are to be listed.
    Returns:
        dict: A dictionary containing the list of group members."""
    client = get_box_client(ctx)
    return box_groups_list_members(client, group_id)


async def box_groups_list_by_user_tool(ctx: Context, user_id: str) -> dict:
    """List all groups that a specific user belongs to.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        user_id (str): The ID of the user whose groups are to be listed.
    Returns:
        dict: A dictionary containing the list of groups the user belongs to."""
    client = get_box_client(ctx)
    return box_groups_list_by_user(client, user_id)
