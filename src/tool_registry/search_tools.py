from mcp.server.fastmcp import FastMCP

from tools.box_tools_search import (
    box_search_folder_by_name_tool,
    box_search_tool,
)


def register_search_tools(mcp: FastMCP):
    mcp.tool()(box_search_tool)
    mcp.tool()(box_search_folder_by_name_tool)
