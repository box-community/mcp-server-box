# Box Tools Shared Links

This document describes the tools available in the `box_tools_shared_links` module for managing shared links for files, folders, and web links in Box.

## Available Tools

### 1. `box_shared_link_file_get_tool`
Get a shared link for a file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file

### 2. `box_shared_link_file_create_or_update_tool`
Create or update a shared link for a file.
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

...and more tools for folders and web links. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_shared_links.py` for implementation details.