from typing import cast

from box_ai_agents_toolkit import BoxClient, authorize_app
from mcp.server.fastmcp import Context

from server_context import BoxContext


def get_box_client(ctx: Context) -> BoxClient:
    """Helper function to get Box client from context.

    This works for both OAuth and CCG modes:
    - OAuth mode: Creates a client from the Bearer token in the request
    - CCG mode: Returns the pre-initialized client
    """
    box_context = cast(BoxContext, ctx.request_context.lifespan_context)

    # For OAuth mode, we need the request to extract the token
    if box_context.client is None:
        # Store the request in the context if not already there
        if box_context.request is None and ctx.request_context.request is not None:
            box_context.request = ctx.request_context.request

    # Use the new get_active_client() method which handles both modes
    return box_context.get_active_client()


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
