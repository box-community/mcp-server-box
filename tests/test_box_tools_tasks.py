from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

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


@pytest.mark.asyncio
async def test_box_task_assign_by_email_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    email = "user@example.com"
    with (
        patch("tools.box_tools_tasks.box_task_assign_by_email") as mock_assign,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_assign.return_value = {
            "assignment": {"id": "1", "assigned_to": {"login": email}}
        }
        result = await box_task_assign_by_email_tool(ctx, task_id, email)
        assert isinstance(result, dict)
        assert "assignment" in result
        assert result["assignment"]["assigned_to"]["login"] == email


@pytest.mark.asyncio
async def test_box_task_assign_by_user_id_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    user_id = "67890"
    with (
        patch("tools.box_tools_tasks.box_task_assign_by_user_id") as mock_assign,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_assign.return_value = {
            "assignment": {"id": "1", "assigned_to": {"id": user_id}}
        }
        result = await box_task_assign_by_user_id_tool(ctx, task_id, user_id)
        assert isinstance(result, dict)
        assert "assignment" in result
        assert result["assignment"]["assigned_to"]["id"] == user_id


@pytest.mark.asyncio
async def test_box_task_assignment_details_tool():
    ctx = MagicMock(spec=Context)
    assignment_id = "54321"
    with (
        patch("tools.box_tools_tasks.box_task_assignment_details") as mock_details,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_details.return_value = {
            "assignment": {
                "id": assignment_id,
                "resolution_state": "incomplete",
                "message": "Test assignment",
            }
        }
        result = await box_task_assignment_details_tool(ctx, assignment_id)
        assert isinstance(result, dict)
        assert "assignment" in result
        assert result["assignment"]["id"] == assignment_id


@pytest.mark.asyncio
async def test_box_task_assignment_remove_tool():
    ctx = MagicMock(spec=Context)
    assignment_id = "54321"
    with (
        patch("tools.box_tools_tasks.box_task_assignment_remove") as mock_remove,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {"message": "Task assignment removed successfully."}
        result = await box_task_assignment_remove_tool(ctx, assignment_id)
        assert isinstance(result, dict)
        assert "message" in result
        assert "removed successfully" in result["message"]


@pytest.mark.asyncio
async def test_box_task_assignment_update_tool():
    ctx = MagicMock(spec=Context)
    assignment_id = "54321"
    is_positive_outcome = True
    message = "Task completed"
    with (
        patch("tools.box_tools_tasks.box_task_assignment_update") as mock_update,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_update.return_value = {
            "task assignment": {
                "id": assignment_id,
                "resolution_state": "completed",
                "message": message,
            }
        }
        result = await box_task_assignment_update_tool(
            ctx, assignment_id, is_positive_outcome, message
        )
        assert isinstance(result, dict)
        assert "task assignment" in result
        assert result["task assignment"]["message"] == message


@pytest.mark.asyncio
async def test_box_task_assignments_list_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    with (
        patch("tools.box_tools_tasks.box_task_assignments_list") as mock_list,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = {
            "assignments": [
                {"id": "1", "assigned_to": {"name": "User 1"}},
                {"id": "2", "assigned_to": {"name": "User 2"}},
            ]
        }
        result = await box_task_assignments_list_tool(ctx, task_id)
        assert isinstance(result, dict)
        assert "assignments" in result
        assert len(result["assignments"]) == 2


@pytest.mark.asyncio
async def test_box_task_complete_create_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    due_at = datetime(2024, 12, 31, 23, 59, 59)
    message = "Please complete this task"
    with (
        patch("tools.box_tools_tasks.box_task_complete_create") as mock_create,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {
            "task": {
                "id": "1",
                "type": "task",
                "action": "complete",
                "message": message,
                "due_at": due_at.isoformat(),
            }
        }
        result = await box_task_complete_create_tool(ctx, file_id, due_at, message)
        assert isinstance(result, dict)
        assert "task" in result
        assert result["task"]["action"] == "complete"
        assert result["task"]["message"] == message


@pytest.mark.asyncio
async def test_box_task_details_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    with (
        patch("tools.box_tools_tasks.box_task_details") as mock_details,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_details.return_value = {
            "task": {
                "id": task_id,
                "type": "task",
                "action": "review",
                "message": "Please review",
            }
        }
        result = await box_task_details_tool(ctx, task_id)
        assert isinstance(result, dict)
        assert "task" in result
        assert result["task"]["id"] == task_id


@pytest.mark.asyncio
async def test_box_task_file_list_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    with (
        patch("tools.box_tools_tasks.box_task_file_list") as mock_list,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = {
            "tasks": [
                {"id": "1", "action": "review", "message": "Review task"},
                {"id": "2", "action": "complete", "message": "Complete task"},
            ]
        }
        result = await box_task_file_list_tool(ctx, file_id)
        assert isinstance(result, dict)
        assert "tasks" in result
        assert len(result["tasks"]) == 2


@pytest.mark.asyncio
async def test_box_task_remove_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    with (
        patch("tools.box_tools_tasks.box_task_remove") as mock_remove,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {"message": "Task removed successfully."}
        result = await box_task_remove_tool(ctx, task_id)
        assert isinstance(result, dict)
        assert "message" in result
        assert "removed successfully" in result["message"]


@pytest.mark.asyncio
async def test_box_task_review_create_tool():
    ctx = MagicMock(spec=Context)
    file_id = "12345"
    due_at = datetime(2024, 12, 31, 23, 59, 59)
    message = "Please review this file"
    requires_all_assignees = True
    with (
        patch("tools.box_tools_tasks.box_task_review_create") as mock_create,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {
            "task": {
                "id": "1",
                "type": "task",
                "action": "review",
                "message": message,
                "due_at": due_at.isoformat(),
                "completion_rule": "all_assignees",
            }
        }
        result = await box_task_review_create_tool(
            ctx, file_id, due_at, message, requires_all_assignees
        )
        assert isinstance(result, dict)
        assert "task" in result
        assert result["task"]["action"] == "review"
        assert result["task"]["message"] == message
        assert result["task"]["completion_rule"] == "all_assignees"


@pytest.mark.asyncio
async def test_box_task_update_tool():
    ctx = MagicMock(spec=Context)
    task_id = "12345"
    due_at = datetime(2025, 1, 15, 23, 59, 59)
    message = "Updated task message"
    with (
        patch("tools.box_tools_tasks.box_task_update") as mock_update,
        patch("tools.box_tools_tasks.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_update.return_value = {
            "task": {
                "id": task_id,
                "type": "task",
                "message": message,
                "due_at": due_at.isoformat(),
            }
        }
        result = await box_task_update_tool(ctx, task_id, due_at, message)
        assert isinstance(result, dict)
        assert "task" in result
        assert result["task"]["message"] == message
