# Box Tools Search

This document describes the tools available in the `box_tools_search` module for searching files and folders in Box.

## Available Tools

### 1. `box_search_tool`
Search for files in Box with a query.
- **Arguments:**
  - `ctx`: Request context
  - `query`: Search query
  - `file_extensions`: List of file extensions (optional)
  - `where_to_look_for_query`: List of content types (optional)
  - `ancestor_folder_ids`: List of ancestor folder IDs (optional)

### 2. `box_search_folder_by_name_tool`
Locate a folder in Box by its name.
- **Arguments:**
  - `ctx`: Request context
  - `folder_name`: Name of the folder

---

Refer to `src/tools/box_tools_search.py` for implementation details.