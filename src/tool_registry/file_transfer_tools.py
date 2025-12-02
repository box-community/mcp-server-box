from mcp.server.fastmcp import FastMCP

from tools.box_tools_file_transfer import (
    box_file_download_tool,
    box_file_upload_tool,
)


def register_file_transfer_tools(mcp: FastMCP):
    mcp.tool()(box_file_download_tool)
    mcp.tool()(box_file_upload_tool)
