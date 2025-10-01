from mcp.server.fastmcp import FastMCP

from tools.box_tools_shared_links import (
    box_shared_link_file_create_or_update_tool,
    box_shared_link_file_find_by_shared_link_url_tool,
    box_shared_link_file_get_tool,
    box_shared_link_file_remove_tool,
    box_shared_link_folder_create_or_update_tool,
    box_shared_link_folder_find_by_shared_link_url_tool,
    box_shared_link_folder_get_tool,
    box_shared_link_folder_remove_tool,
    box_shared_link_web_link_create_or_update_tool,
    box_shared_link_web_link_find_by_shared_link_url_tool,
    box_shared_link_web_link_get_tool,
    box_shared_link_web_link_remove_tool,
)


def register_shared_link_tools(mcp: FastMCP):
    # Shared Link - File Tools
    mcp.tool()(box_shared_link_file_get_tool)
    mcp.tool()(box_shared_link_file_create_or_update_tool)
    mcp.tool()(box_shared_link_file_remove_tool)
    mcp.tool()(box_shared_link_file_find_by_shared_link_url_tool)

    # Shared Link - Folder Tools
    mcp.tool()(box_shared_link_folder_get_tool)
    mcp.tool()(box_shared_link_folder_create_or_update_tool)
    mcp.tool()(box_shared_link_folder_remove_tool)
    mcp.tool()(box_shared_link_folder_find_by_shared_link_url_tool)

    # Shared Link - Web Link Tools
    mcp.tool()(box_shared_link_web_link_get_tool)
    mcp.tool()(box_shared_link_web_link_create_or_update_tool)
    mcp.tool()(box_shared_link_web_link_remove_tool)
    mcp.tool()(box_shared_link_web_link_find_by_shared_link_url_tool)
