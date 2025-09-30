from mcp.server.fastmcp import FastMCP

from tools.box_tools_folders import (
    box_list_folder_content_by_folder_id,
    box_manage_folder_tool,
)


def register_folder_tools(mcp: FastMCP):
    mcp.tool()(box_list_folder_content_by_folder_id)
    mcp.tool()(box_manage_folder_tool)
