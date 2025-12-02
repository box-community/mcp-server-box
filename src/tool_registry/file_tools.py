from mcp.server.fastmcp import FastMCP

from tools.box_tools_file import (
    box_file_copy_tool,
    box_file_delete_tool,
    box_file_info_tool,
    box_file_lock_tool,
    box_file_move_tool,
    box_file_rename_tool,
    box_file_retention_date_clear_tool,
    box_file_retention_date_set_tool,
    box_file_set_description_tool,
    box_file_set_download_company_tool,
    box_file_set_download_open_tool,
    box_file_set_download_reset_tool,
    box_file_tag_add_tool,
    box_file_tag_list_tool,
    box_file_tag_remove_tool,
    box_file_thumbnail_download_tool,
    box_file_thumbnail_url_tool,
    box_file_unlock_tool,
)


def register_file_tools(mcp: FastMCP):
    mcp.tool()(box_file_info_tool)
    mcp.tool()(box_file_copy_tool)
    mcp.tool()(box_file_delete_tool)
    mcp.tool()(box_file_move_tool)
    mcp.tool()(box_file_rename_tool)
    mcp.tool()(box_file_set_description_tool)
    mcp.tool()(box_file_retention_date_set_tool)
    mcp.tool()(box_file_retention_date_clear_tool)
    mcp.tool()(box_file_lock_tool)
    mcp.tool()(box_file_unlock_tool)
    mcp.tool()(box_file_set_download_open_tool)
    mcp.tool()(box_file_set_download_company_tool)
    mcp.tool()(box_file_set_download_reset_tool)
    mcp.tool()(box_file_tag_list_tool)
    mcp.tool()(box_file_tag_add_tool)
    mcp.tool()(box_file_tag_remove_tool)
    mcp.tool()(box_file_thumbnail_url_tool)
    mcp.tool()(box_file_thumbnail_download_tool)
