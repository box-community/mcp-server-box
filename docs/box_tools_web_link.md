# Box Tools Web Link

This document describes the tools available in the `box_tools_web_link` module for web link creation and management in Box.

## Available Tools

### 1. `box_web_link_create_tool`
Create a Box web link.
- **Arguments:**
  - `ctx`: Request context
  - `url`: URL of the web link
  - `parent_folder_id`: Parent folder ID
  - `name`: Name of the web link (optional)
  - `description`: Description (optional)

### 2. `box_web_link_get_by_id_tool`
Get a Box web link by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `web_link_id`: ID of the web link

### 3. `box_web_link_update_by_id_tool`
Update a Box web link by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `web_link_id`: ID of the web link
  - `url`: New URL

...and more tools for deleting web links. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_web_link.py` for implementation details.