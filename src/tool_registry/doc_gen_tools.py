from mcp.server.fastmcp import FastMCP

from tools.box_tools_docgen import (
    box_docgen_create_batch_tool,
    box_docgen_create_single_file_from_user_input_tool,
    box_docgen_get_job_by_id_tool,
    box_docgen_list_jobs_by_batch_tool,
    box_docgen_list_jobs_tool,
    box_docgen_template_create_tool,
    box_docgen_template_get_by_id_tool,
    box_docgen_template_get_by_name_tool,
    box_docgen_template_list_jobs_tool,
    # box_docgen_template_delete_tool, # very dangerous tool, use with caution
    box_docgen_template_list_tags_tool,
    box_docgen_template_list_tool,
)


def register_doc_gen_tools(mcp: FastMCP):
    mcp.tool()(box_docgen_create_batch_tool)
    mcp.tool()(box_docgen_get_job_by_id_tool)
    mcp.tool()(box_docgen_list_jobs_tool)
    mcp.tool()(box_docgen_list_jobs_by_batch_tool)
    mcp.tool()(box_docgen_template_create_tool)
    mcp.tool()(box_docgen_template_list_tool)
    # mcp.tool()(box_docgen_template_delete_tool) # very dangerous tool, use with caution
    mcp.tool()(box_docgen_template_get_by_id_tool)
    mcp.tool()(box_docgen_template_list_tags_tool)
    mcp.tool()(box_docgen_template_list_jobs_tool)
    mcp.tool()(box_docgen_template_get_by_name_tool)
    mcp.tool()(box_docgen_create_single_file_from_user_input_tool)
