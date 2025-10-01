# Box Tools Collaboration

This document describes the tools available in the `box_tools_collaboration` module for managing collaborations on Box files and folders.

## Available Tools

### 1. `box_collaboration_list_by_file_tool`
List all collaborations on a specific file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file

### 2. `box_collaboration_list_by_folder_tool`
List all collaborations on a specific folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder

### 3. `box_collaboration_delete_tool`
Delete a specific collaboration.
- **Arguments:**
  - `ctx`: Request context
  - `collaboration_id`: ID of the collaboration

### 4. `box_collaboration_file_group_by_group_id_tool`
Add a group as a collaborator to a file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file
  - `group_id`: ID of the group
  - `role`: Collaboration role (default: "editor")

...and more tools for user/group collaboration management. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_collaboration.py` for implementation details.