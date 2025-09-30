from mcp.server.fastmcp import FastMCP

from box_tools_generic import (
    box_authorize_app_tool,
    box_who_am_i,
)


def register_generic_tools(mcp: FastMCP):
    mcp.tool()(box_who_am_i)
    mcp.tool()(box_authorize_app_tool)
