# Box Tools Files

This document describes the tools available in the `box_tools_files` module for file operations in Box.

## Available Tools

### 1. `box_read_tool`
Read and extract text content from a file in Box.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file

### 2. `box_upload_file_from_path_tool`
Upload a file to Box from a server filesystem path. Supports both text and binary files with optional file renaming.
- **Arguments:**
  - `ctx`: Request context
  - `file_path`: Path to the file on the filesystem
  - `folder_id`: Destination folder ID (default: "0" for root)
  - `new_file_name`: Optional new name for the file

### 3. `box_upload_file_from_content_tool`
Upload content (text or binary) as a file to Box. Supports base64-encoded content.
- **Arguments:**
  - `ctx`: Request context
  - `file_content`: Content to upload (string or base64-encoded)
  - `file_name`: Name for the new file
  - `folder_id`: Destination folder ID (default: "0" for root)

### 4. `box_download_file_tool`
Download a file from Box and return its content. Supports text files (returns content directly) and images (returns base64-encoded). Can optionally save file locally.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file to download
  - `local_save_path`: Optional local filesystem path to save the file

---

Refer to `src/tools/box_tools_files.py` for implementation details.
