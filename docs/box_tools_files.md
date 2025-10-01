# Box Tools Files

This document describes the tools available in the `box_tools_files` module for file operations in Box.

## Available Tools

### 1. `box_read_tool`
Read the text content of a file in Box.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file

### 2. `box_upload_file_from_path_tool`
Upload a file to Box from a filesystem path.
- **Arguments:**
  - `ctx`: Request context
  - `file_path`: Path to the file
  - `folder_id`: Destination folder ID (default: "0")
  - `new_file_name`: Optional new name

...and more tools for downloading files, extracting text, and handling images/documents. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_files.py` for implementation details.