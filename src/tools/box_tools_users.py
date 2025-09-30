
from box_ai_agents_toolkit import (
    box_users_list,
    box_users_locate_by_name,
    box_users_locate_by_email,
    box_users_search_by_name_or_email,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_users_list_tool(ctx: Context) -> dict:
    """List all users in the Box account.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
    Returns:
        dict: A dictionary containing the list of users."""
    client = get_box_client(ctx)
    return box_users_list(client)


async def box_users_locate_by_name_tool(ctx: Context, name: str) -> dict:
    """Locate a user by their name. This is an exact match search.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        name (str): The name of the user to locate.
    Returns:
        dict: A dictionary containing the user information if found, otherwise a message with no user found."""
    client = get_box_client(ctx)
    return box_users_locate_by_name(client, name)


async def box_users_locate_by_email_tool(ctx: Context, email: str) -> dict:
    """Locate a user by their email address. This is an exact match search.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        email (str): The email address of the user to locate.
    Returns:
        dict: A dictionary containing the user information if found, otherwise a message with no user found."""
    client = get_box_client(ctx)
    return box_users_locate_by_email(client, email)


async def box_users_search_by_name_or_email_tool(ctx: Context, query: str) -> dict:
    """Search for users by name or email. This is a partial match search.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        query (str): The search query to match against user names and email addresses.
    Returns:
        dict: A dictionary containing the list of matching users."""
    client = get_box_client(ctx)
    return box_users_search_by_name_or_email(client, query)
