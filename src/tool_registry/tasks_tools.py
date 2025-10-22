from mcp.server.fastmcp import FastMCP

from tools.box_tools_tasks import (
    box_task_assign_by_email_tool,
    box_task_assign_by_user_id_tool,
    box_task_assignment_details_tool,
    box_task_assignment_remove_tool,
    box_task_assignment_update_tool,
    box_task_assignments_list_tool,
    box_task_complete_create_tool,
    box_task_details_tool,
    box_task_file_list_tool,
    box_task_remove_tool,
    box_task_review_create_tool,
    box_task_update_tool,
)


def register_tasks_tools(mcp: FastMCP):
    mcp.tool()(box_task_assign_by_email_tool)
    mcp.tool()(box_task_assign_by_user_id_tool)
    mcp.tool()(box_task_assignment_details_tool)
    mcp.tool()(box_task_assignment_remove_tool)
    mcp.tool()(box_task_assignment_update_tool)
    mcp.tool()(box_task_assignments_list_tool)
    mcp.tool()(box_task_complete_create_tool)
    mcp.tool()(box_task_details_tool)
    mcp.tool()(box_task_file_list_tool)
    mcp.tool()(box_task_remove_tool)
    mcp.tool()(box_task_review_create_tool)
    mcp.tool()(box_task_update_tool)
