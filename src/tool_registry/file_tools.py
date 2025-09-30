from mcp.server.fastmcp import FastMCP

from tools.box_tools_files import (
    box_download_file_tool,
    box_read_tool,
    box_upload_file_from_content_tool,
    box_upload_file_from_path_tool,
)


def register_file_tools(mcp: FastMCP):
    mcp.tool()(box_read_tool)
    mcp.tool()(box_download_file_tool)
    mcp.tool()(box_upload_file_from_content_tool)
    mcp.tool()(box_upload_file_from_path_tool)
