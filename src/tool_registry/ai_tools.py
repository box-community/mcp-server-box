from mcp.server.fastmcp import FastMCP

from tools.box_tools_ai import (
    box_ai_ask_file_multi_tool,
    box_ai_ask_file_single_tool,
    box_ai_ask_hub_tool,
    box_ai_extract_freeform_tool,
    box_ai_extract_structured_enhanced_using_fields_tool,
    box_ai_extract_structured_enhanced_using_template_tool,
    box_ai_extract_structured_using_fields_tool,
    box_ai_extract_structured_using_template_tool,
)


def register_ai_tools(mcp: FastMCP):
    mcp.tool()(box_ai_ask_file_single_tool)
    mcp.tool()(box_ai_ask_file_multi_tool)
    mcp.tool()(box_ai_ask_hub_tool)
    mcp.tool()(box_ai_extract_freeform_tool)
    mcp.tool()(box_ai_extract_structured_using_fields_tool)
    mcp.tool()(box_ai_extract_structured_using_template_tool)
    mcp.tool()(box_ai_extract_structured_enhanced_using_fields_tool)
    mcp.tool()(box_ai_extract_structured_enhanced_using_template_tool)
