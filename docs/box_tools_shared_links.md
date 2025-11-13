# Box Tools Shared Links

This document describes the tools available in the `box_tools_shared_links` module for managing shared links for files, folders, and web links in Box.

## Available Tools

### File Shared Links

#### 1. `box_shared_link_file_get_tool`
Get a shared link for a file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file

#### 2. `box_shared_link_file_create_or_update_tool`
Create or update a shared link for a file with access level, download/preview/edit permissions, password, and expiration.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `access`: Access level (optional)
  - `can_download`: Can download (optional)
  - `can_preview`: Can preview (optional)
  - `can_edit`: Can edit (optional)
  - `password`: Password (optional)
  - `vanity_name`: Vanity name (optional)
  - `unshared_at`: Expiration date (optional)

#### 3. `box_shared_link_file_remove_tool`
Remove a shared link from a file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file

#### 4. `box_shared_link_file_find_by_shared_link_url_tool`
Find a file by its shared link URL (supports password-protected links).
- **Arguments:**
  - `ctx`: Request context
  - `shared_link_url`: The shared link URL
  - `password`: Password if link is protected (optional)

### Folder Shared Links

#### 5. `box_shared_link_folder_get_tool`
Get a shared link for a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder

#### 6. `box_shared_link_folder_create_or_update_tool`
Create or update a shared link for a folder with configurable permissions.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder
  - `access`: Access level (optional)
  - `can_download`: Can download (optional)
  - `can_preview`: Can preview (optional)
  - `can_edit`: Can edit (optional)
  - `password`: Password (optional)
  - `vanity_name`: Vanity name (optional)
  - `unshared_at`: Expiration date (optional)

#### 7. `box_shared_link_folder_remove_tool`
Remove a shared link from a folder.
- **Arguments:**
  - `ctx`: Request context
  - `folder_id`: ID of the folder

#### 8. `box_shared_link_folder_find_by_shared_link_url_tool`
Find a folder by its shared link URL.
- **Arguments:**
  - `ctx`: Request context
  - `shared_link_url`: The shared link URL
  - `password`: Password if link is protected (optional)

### Web Link Shared Links

#### 9. `box_shared_link_web_link_create_or_update_tool`
Create or update a shared link for a web link.
- **Arguments:**
  - `ctx`: Request context
  - `web_link_id`: ID of the web link
  - `access`: Access level (optional)
  - `password`: Password (optional)
  - `vanity_name`: Vanity name (optional)
  - `unshared_at`: Expiration date (optional)

#### 10. `box_shared_link_web_link_get_tool`
Get a shared link for a web link.
- **Arguments:**
  - `ctx`: Request context
  - `web_link_id`: ID of the web link

#### 11. `box_shared_link_web_link_remove_tool`
Remove a shared link from a web link.
- **Arguments:**
  - `ctx`: Request context
  - `web_link_id`: ID of the web link

#### 12. `box_shared_link_web_link_find_by_shared_link_url_tool`
Find a web link by its shared link URL.
- **Arguments:**
  - `ctx`: Request context
  - `shared_link_url`: The shared link URL
  - `password`: Password if link is protected (optional)

---

Refer to `src/tools/box_tools_shared_links.py` for implementation details.
