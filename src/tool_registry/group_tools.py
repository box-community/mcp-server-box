from mcp.server.fastmcp import FastMCP

from tools.box_tools_groups import (
    box_groups_list_by_user_tool,
    box_groups_list_members_tool,
    box_groups_search_tool,
)


def register_group_tools(mcp: FastMCP):
    mcp.tool()(box_groups_search_tool)
    mcp.tool()(box_groups_list_members_tool)
    mcp.tool()(box_groups_list_by_user_tool)
