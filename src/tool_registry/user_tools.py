from mcp.server.fastmcp import FastMCP

from tools.box_tools_users import (
    box_users_list_tool,
    box_users_locate_by_email_tool,
    box_users_locate_by_name_tool,
    box_users_search_by_name_or_email_tool,
)


def register_user_tools(mcp: FastMCP):
    mcp.tool()(box_users_list_tool)
    mcp.tool()(box_users_locate_by_email_tool)
    mcp.tool()(box_users_locate_by_name_tool)
    mcp.tool()(box_users_search_by_name_or_email_tool)
