from mcp.server.fastmcp import FastMCP

from tools.box_tools_file_representation import box_file_text_extract_tool


def register_file_tools(mcp: FastMCP):
    mcp.tool()(box_file_text_extract_tool)
