# Box Tools Folders

This document describes the tools available in the `box_tools_folders` module for folder operations in Box.

## Available Tools

### 1. `box_folder_info_tool`
Retrieve detailed information about a specific folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder

### 2. `box_folder_items_list_tool`
List items in a folder with optional recursive traversal.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder
  - `is_recursive`: Whether to list recursively (default: False)

### 3. `box_folder_create_tool`
Create a new folder in Box.
- **Arguments:**
  - `ctx`: Request context
  - `name`: Name of the new folder
  - `parent_folder_id`: Parent folder ID (default: "0" for root)

### 4. `box_folder_rename_tool`
Rename a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to rename
  - `new_name`: New folder name

### 5. `box_folder_move_tool`
Move a folder to a new location in Box.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to move
  - `destination_parent_folder_id`: ID of the new parent folder

### 6. `box_folder_copy_tool`
Copy a folder to a new location in Box with optional name change.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to copy
  - `destination_parent_folder_id`: ID of the destination parent folder
  - `name`: Optional new name for the copied folder

### 7. `box_folder_delete_tool`
Delete a folder from Box with optional recursive deletion.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to delete
  - `recursive`: Whether to recursively delete contents (default: False)

### 8. `box_folder_set_description_tool`
Set the description text for a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `description`: Description text

### 9. `box_folder_favorites_add_tool`
Add a folder to the user's favorites.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to add

### 10. `box_folder_favorites_remove_tool`
Remove a folder from the user's favorites.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder to remove

### 11. `box_folder_tag_add_tool`
Add a tag to a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `tag`: Name of the tag to add

### 12. `box_folder_tag_remove_tool`
Remove a tag from a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `tag`: Name of the tag to remove

### 13. `box_folder_list_tags_tool`
List tags associated with a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder

### 14. `box_folder_set_collaboration_tool`
Set collaboration settings (invitation and visibility rules) for a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `is_collaboration_restricted_to_enterprise`: Collaboration settings configuration

### 15. `box_folder_set_sync_tool`
Set the sync state for a folder (synced, not_synced, partially_synced).
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `sync_state`: Sync state value

### 16. `box_folder_set_upload_email_tool`
Enable or disable and configure upload email address for a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `folder_upload_email_access`: Whether to enable upload email (default: True)

---

Refer to `src/tools/box_tools_folders.py` for implementation details.
