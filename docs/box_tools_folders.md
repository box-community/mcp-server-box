# Box Tools Folders

This document describes the tools available in the `box_tools_folders` module for folder operations in Box.

## Available Tools

### 1. `box_list_folder_content_by_folder_id`
List the content of a folder by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder
  - `is_recursive`: Whether to list recursively (default: False)

### 2. `box_manage_folder_tool`
Create, update, or delete a folder.
- **Arguments:**
  - `ctx`: Request context
  - `action`: Action to perform (create, update, delete)
  - `folder_id`: Folder ID (required for delete/update)
  - `name`: Folder name (required for create)
  - `parent_id`: Parent folder ID (optional)

---

Refer to `src/tools/box_tools_folders.py` for implementation details.