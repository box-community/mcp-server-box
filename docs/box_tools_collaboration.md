# Box Tools Collaboration

This document describes the tools available in the `box_tools_collaboration` module for managing collaborations on Box files and folders.

## Available Tools

### Collaboration Listing

#### 1. `box_collaboration_list_by_file_tool`
List all collaborations on a specific file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file

#### 2. `box_collaboration_list_by_folder_tool`
List all collaborations on a specific folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder

### Collaboration Management

#### 3. `box_collaboration_delete_tool`
Delete a specific collaboration.
- **Arguments:**
  - `ctx`: Request context
  - `collaboration_id`: ID of the collaboration

#### 4. `box_collaboration_update_tool`
Update a collaboration's role, status, expiration date, and visibility settings.
- **Arguments:**
  - `ctx`: Request context
  - `collaboration_id`: ID of the collaboration
  - `role`: New collaboration role
  - Additional optional parameters for expiration and visibility

### File Collaboration Creation

#### 5. `box_collaboration_file_group_by_group_id_tool`
Create a collaboration on a file with a group specified by group ID (supports various roles and access settings).
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file
  - `group_id`: ID of the group
  - `role`: Collaboration role (default: "editor")

#### 6. `box_collaboration_file_user_by_user_id_tool`
Create a collaboration on a file with a user specified by user ID.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file
  - `user_id`: ID of the user
  - `role`: Collaboration role (default: "editor")

#### 7. `box_collaboration_file_user_by_user_login_tool`
Create a collaboration on a file with a user specified by user login/email.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file
  - `user_login`: Email or login of the user
  - `role`: Collaboration role (default: "editor")

### Folder Collaboration Creation

#### 8. `box_collaboration_folder_group_by_group_id_tool`
Create a collaboration on a folder with a group specified by group ID.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder
  - `group_id`: ID of the group
  - `role`: Collaboration role (default: "editor")

#### 9. `box_collaboration_folder_user_by_user_id_tool`
Create a collaboration on a folder with a user specified by user ID.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder
  - `user_id`: ID of the user
  - `role`: Collaboration role (default: "editor")

#### 10. `box_collaboration_folder_user_by_user_login_tool`
Create a collaboration on a folder with a user specified by user login/email.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the Box folder
  - `user_login`: Email or login of the user
  - `role`: Collaboration role (default: "editor")

---

Refer to `src/tools/box_tools_collaboration.py` for implementation details.
