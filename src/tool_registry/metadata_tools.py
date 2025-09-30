from mcp.server.fastmcp import FastMCP

from tools.box_tools_metadata import (
    box_metadata_delete_instance_on_file_tool,
    box_metadata_get_instance_on_file_tool,
    box_metadata_set_instance_on_file_tool,
    box_metadata_template_create_tool,
    box_metadata_template_get_by_name_tool,
    box_metadata_update_instance_on_file_tool,
)


def register_metadata_tools(mcp: FastMCP):
    mcp.tool()(box_metadata_template_create_tool)
    mcp.tool()(box_metadata_template_get_by_name_tool)
    mcp.tool()(box_metadata_get_instance_on_file_tool)
    mcp.tool()(box_metadata_set_instance_on_file_tool)
    mcp.tool()(box_metadata_update_instance_on_file_tool)
    mcp.tool()(box_metadata_delete_instance_on_file_tool)
