from datetime import datetime

from box_ai_agents_toolkit import (
    box_task_assign_by_email,
    box_task_assign_by_user_id,
    box_task_assignment_details,
    box_task_assignment_remove,
    box_task_assignment_update,
    box_task_assignments_list,
    box_task_complete_create,
    box_task_details,
    box_task_file_list,
    box_task_remove,
    box_task_review_create,
    box_task_update,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_task_assign_by_email_tool(ctx: Context, task_id: str, email: str) -> dict:
    """
    Assign a Box task to a user via email.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to assign.
        email (str): The email of the user to assign the task to.
    Returns:
        dict: The response from the Box API after assigning the task.
    """
    box_client = get_box_client(ctx)
    response = box_task_assign_by_email(box_client, task_id, email)
    return response


async def box_task_assign_by_user_id_tool(
    ctx: Context, task_id: str, user_id: str
) -> dict:
    """
    Assign a Box task to a user via user ID.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to assign.
        user_id (str): The ID of the user to assign the task to.
    Returns:
        dict: The response from the Box API after assigning the task.
    """
    box_client = get_box_client(ctx)
    response = box_task_assign_by_user_id(box_client, task_id, user_id)
    return response


async def box_task_assignment_details_tool(ctx: Context, assignment_id: str) -> dict:
    """
    Get details of a Box task assignment.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        assignment_id (str): The ID of the task assignment.
    Returns:
        dict: The response from the Box API with the task assignment details.
    """
    box_client = get_box_client(ctx)
    response = box_task_assignment_details(box_client, assignment_id)
    return response


async def box_task_assignment_remove_tool(ctx: Context, assignment_id: str) -> dict:
    """
    Remove a Box task assignment.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        assignment_id (str): The ID of the task assignment to remove.
    Returns:
        dict: The response from the Box API after removing the task assignment.
    """
    box_client = get_box_client(ctx)
    response = box_task_assignment_remove(box_client, assignment_id)
    return response


async def box_task_assignment_update_tool(
    ctx: Context,
    assignment_id: str,
    is_positive_outcome: bool,
    message: str | None = None,
) -> dict:
    """
    Update a Box task assignment to mark it as complete or review outcome.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        assignment_id (str): The ID of the task assignment to update.
        is_positive_outcome (bool): For review tasks: True for approved, False for rejected. For complete tasks: True for completed, False for incomplete.
        message (str | None): Optional message or description for the task assignment update.
    Returns:
        dict: The response from the Box API after updating the task assignment.
    """
    box_client = get_box_client(ctx)
    response = box_task_assignment_update(
        box_client, assignment_id, is_positive_outcome, message
    )
    return response


async def box_task_assignments_list_tool(ctx: Context, task_id: str) -> dict:
    """
    List all assignments associated with a Box task.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to list assignments for.
    Returns:
        dict: The response from the Box API with the list of task assignments.
    """
    box_client = get_box_client(ctx)
    response = box_task_assignments_list(box_client, task_id)
    return response


async def box_task_complete_create_tool(
    ctx: Context,
    file_id: str,
    due_at: datetime | None = None,
    message: str | None = None,
    requires_all_assignees_to_complete: bool = False,
) -> dict:
    """
    Create a new completion task for a Box file.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to create the task for.
        due_at (datetime | None): Optional due date for the task.
        message (str | None): Optional message or description for the task.
        requires_all_assignees_to_complete (bool): Whether all assignees must complete the task. Defaults to False.
    Returns:
        dict: The response from the Box API after creating the completion task.
    """
    box_client = get_box_client(ctx)
    response = box_task_complete_create(
        box_client, file_id, due_at, message, requires_all_assignees_to_complete
    )
    return response


async def box_task_details_tool(ctx: Context, task_id: str) -> dict:
    """
    Get details of a Box task.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to retrieve details for.
    Returns:
        dict: The response from the Box API with the task details.
    """
    box_client = get_box_client(ctx)
    response = box_task_details(box_client, task_id)
    return response


async def box_task_file_list_tool(ctx: Context, file_id: str) -> dict:
    """
    List all tasks associated with a Box file.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to list tasks for.
    Returns:
        dict: The response from the Box API with the list of tasks.
    """
    box_client = get_box_client(ctx)
    response = box_task_file_list(box_client, file_id)
    return response


async def box_task_remove_tool(ctx: Context, task_id: str) -> dict:
    """
    Remove a Box task.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to remove.
    Returns:
        dict: The response from the Box API after removing the task.
    """
    box_client = get_box_client(ctx)
    response = box_task_remove(box_client, task_id)
    return response


async def box_task_review_create_tool(
    ctx: Context,
    file_id: str,
    due_at: datetime | None = None,
    message: str | None = None,
    requires_all_assignees_to_complete: bool = False,
) -> dict:
    """
    Create a new review task for a Box file.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to create the task for.
        due_at (datetime | None): Optional due date for the task.
        message (str | None): Optional message or description for the task.
        requires_all_assignees_to_complete (bool): Whether all assignees must complete the task. Defaults to False.
    Returns:
        dict: The response from the Box API after creating the review task.
    """
    box_client = get_box_client(ctx)
    response = box_task_review_create(
        box_client, file_id, due_at, message, requires_all_assignees_to_complete
    )
    return response


async def box_task_update_tool(
    ctx: Context,
    task_id: str,
    due_at: datetime | None = None,
    message: str | None = None,
    requires_all_assignees_to_complete: bool = False,
) -> dict:
    """
    Update a Box task.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        task_id (str): The ID of the task to update.
        due_at (datetime | None): Optional new due date for the task.
        message (str | None): Optional new message or description for the task.
        requires_all_assignees_to_complete (bool): Whether all assignees must complete the task. Defaults to False.
    Returns:
        dict: The response from the Box API after updating the task.
    """
    box_client = get_box_client(ctx)
    response = box_task_update(
        box_client, task_id, due_at, message, requires_all_assignees_to_complete
    )
    return response
