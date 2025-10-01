from mcp.server.fastmcp import FastMCP

from tools.box_tools_web_link import (
    box_web_link_create_tool,
    box_web_link_delete_by_id_tool,
    box_web_link_get_by_id_tool,
    box_web_link_update_by_id_tool,
)


def register_web_link_tools(mcp: FastMCP):
    mcp.tool()(box_web_link_create_tool)
    mcp.tool()(box_web_link_get_by_id_tool)
    mcp.tool()(box_web_link_update_by_id_tool)
    mcp.tool()(box_web_link_delete_by_id_tool)
