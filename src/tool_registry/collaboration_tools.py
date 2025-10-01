from mcp.server.fastmcp import FastMCP

from tools.box_tools_collaboration import (
    box_collaboration_delete_tool,
    box_collaboration_file_group_by_group_id_tool,
    box_collaboration_file_user_by_user_id_tool,
    box_collaboration_file_user_by_user_login_tool,
    box_collaboration_folder_group_by_group_id_tool,
    box_collaboration_folder_user_by_user_id_tool,
    box_collaboration_folder_user_by_user_login_tool,
    box_collaboration_list_by_file_tool,
    box_collaboration_list_by_folder_tool,
    box_collaboration_update_tool,
)


def register_collaboration_tools(mcp: FastMCP):
    # Collaboration Tools
    mcp.tool()(box_collaboration_list_by_file_tool)
    mcp.tool()(box_collaboration_list_by_folder_tool)
    mcp.tool()(box_collaboration_delete_tool)
    mcp.tool()(box_collaboration_file_user_by_user_id_tool)
    mcp.tool()(box_collaboration_file_user_by_user_login_tool)
    mcp.tool()(box_collaboration_folder_user_by_user_id_tool)
    mcp.tool()(box_collaboration_folder_user_by_user_login_tool)
    mcp.tool()(box_collaboration_file_group_by_group_id_tool)
    mcp.tool()(box_collaboration_folder_group_by_group_id_tool)
    mcp.tool()(box_collaboration_update_tool)
