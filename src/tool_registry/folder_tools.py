from mcp.server.fastmcp import FastMCP

from tools.box_tools_folders import (
    box_folder_copy_tool,
    box_folder_create_tool,
    box_folder_delete_tool,
    box_folder_favorites_add_tool,
    box_folder_favorites_remove_tool,
    box_folder_info_tool,
    box_folder_items_list_tool,
    box_folder_list_tags_tool,
    box_folder_move_tool,
    box_folder_rename_tool,
    box_folder_set_collaboration_tool,
    box_folder_set_description_tool,
    box_folder_set_sync_tool,
    box_folder_set_upload_email_tool,
    box_folder_tag_add_tool,
    box_folder_tag_remove_tool,
)


def register_folder_tools(mcp: FastMCP):
    mcp.tool()(box_folder_copy_tool)
    mcp.tool()(box_folder_create_tool)
    mcp.tool()(box_folder_delete_tool)
    mcp.tool()(box_folder_favorites_add_tool)
    mcp.tool()(box_folder_favorites_remove_tool)
    mcp.tool()(box_folder_info_tool)
    mcp.tool()(box_folder_items_list_tool)
    mcp.tool()(box_folder_list_tags_tool)
    mcp.tool()(box_folder_move_tool)
    mcp.tool()(box_folder_rename_tool)
    mcp.tool()(box_folder_set_collaboration_tool)
    mcp.tool()(box_folder_set_description_tool)
    mcp.tool()(box_folder_set_sync_tool)
    mcp.tool()(box_folder_set_upload_email_tool)
    mcp.tool()(box_folder_tag_add_tool)
    mcp.tool()(box_folder_tag_remove_tool)
