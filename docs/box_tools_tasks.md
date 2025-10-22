# Box Tools Tasks

This document describes the tools available in the `box_tools_tasks` module for managing tasks and task assignments on Box files.

## Available Tools

### Task Creation

#### 1. `box_task_complete_create_tool`
Create a new completion task for a Box file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file to create the task for
  - `due_at`: Optional due date for the task (datetime)
  - `message`: Optional message or description for the task
  - `requires_all_assignees_to_complete`: Whether all assignees must complete the task (default: False)

#### 2. `box_task_review_create_tool`
Create a new review task for a Box file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file to create the task for
  - `due_at`: Optional due date for the task (datetime)
  - `message`: Optional message or description for the task
  - `requires_all_assignees_to_complete`: Whether all assignees must complete the task (default: False)

### Task Management

#### 3. `box_task_details_tool`
Get details of a Box task.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to retrieve details for

#### 4. `box_task_update_tool`
Update a Box task.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to update
  - `due_at`: Optional new due date for the task (datetime)
  - `message`: Optional new message or description for the task
  - `requires_all_assignees_to_complete`: Whether all assignees must complete the task (default: False)

#### 5. `box_task_remove_tool`
Remove a Box task.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to remove

#### 6. `box_task_file_list_tool`
List all tasks associated with a Box file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file to list tasks for

### Task Assignment Management

#### 7. `box_task_assign_by_email_tool`
Assign a Box task to a user via email.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to assign
  - `email`: Email of the user to assign the task to

#### 8. `box_task_assign_by_user_id_tool`
Assign a Box task to a user via user ID.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to assign
  - `user_id`: ID of the user to assign the task to

#### 9. `box_task_assignments_list_tool`
List all assignments associated with a Box task.
- **Arguments:**
  - `ctx`: Request context
  - `task_id`: ID of the task to list assignments for

#### 10. `box_task_assignment_details_tool`
Get details of a Box task assignment.
- **Arguments:**
  - `ctx`: Request context
  - `assignment_id`: ID of the task assignment

#### 11. `box_task_assignment_update_tool`
Update a Box task assignment to mark it as complete or review outcome.
- **Arguments:**
  - `ctx`: Request context
  - `assignment_id`: ID of the task assignment to update
  - `is_positive_outcome`: For review tasks: True for approved, False for rejected. For complete tasks: True for completed, False for incomplete
  - `message`: Optional message or description for the task assignment update

#### 12. `box_task_assignment_remove_tool`
Remove a Box task assignment.
- **Arguments:**
  - `ctx`: Request context
  - `assignment_id`: ID of the task assignment to remove

---

Refer to `src/tools/box_tools_tasks.py` for implementation details.
