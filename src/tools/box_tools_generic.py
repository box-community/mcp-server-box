from typing import cast

from box_ai_agents_toolkit import BoxClient, authorize_app
from mcp.server.fastmcp import Context

from server_context import BoxContext


def get_box_client(ctx: Context) -> BoxClient:
    """Helper function to get Box client from context"""
    client = cast(BoxContext, ctx.request_context.lifespan_context).client
    if client is None:
        raise RuntimeError("Box client is not initialized in the context.")
    return client


async def box_who_am_i(ctx: Context) -> dict:
    """
    Get the current user's information.
    This is also useful to check the connection status.

    return:
        dict: The current user's information.
    """
    box_client = get_box_client(ctx)
    return box_client.users.get_user_me().to_dict()
    # return f"Authenticated as: {current_user.name}"


async def box_authorize_app_tool() -> str:
    """
    Authorize the Box application.
    Start the Box app authorization process

    return:
        str: Message
    """
    result = authorize_app()
    if result:
        return "Box application authorized successfully"
    else:
        return "Box application not authorized"
