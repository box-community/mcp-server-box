# Box Tools Files

This document describes the tools available for file operations in Box. These tools are organized into three categories: file operations, file transfer, and file content extraction.

## File Operations Tools

File operation tools allow you to manage files within Box - getting information, copying, moving, renaming, locking, tagging, and more.

### 1. `box_file_info_tool`
Get detailed information about a file in Box.
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with file metadata (name, size, created date, modified date, etc.)
- **Use Case:** Retrieve file details before performing operations

### 2. `box_file_copy_tool`
Create a copy of a file in a specified destination folder.
- **Arguments:**
  - `file_id` (str): The ID of the file to copy
  - `destination_folder_id` (str): The ID of the destination folder
  - `new_name` (str, optional): Optional new name for the copied file
  - `version_number` (int, optional): Optional specific version number to copy
- **Returns:** dict with copied file information
- **Use Case:** Create backup copies or duplicate files for different workflows

### 3. `box_file_delete_tool`
Delete a file from Box permanently.
- **Arguments:**
  - `file_id` (str): The ID of the file to delete
- **Returns:** dict with success message or error
- **Use Case:** Remove files from Box

### 4. `box_file_move_tool`
Move a file to a different folder.
- **Arguments:**
  - `file_id` (str): The ID of the file to move
  - `destination_folder_id` (str): The ID of the destination folder
- **Returns:** dict with moved file information
- **Use Case:** Reorganize files within folder structure

### 5. `box_file_rename_tool`
Rename a file in Box.
- **Arguments:**
  - `file_id` (str): The ID of the file to rename
  - `new_name` (str): The new name for the file
- **Returns:** dict with renamed file information
- **Use Case:** Update file names for clarity or standardization

### 6. `box_file_set_description_tool`
Set or update the description of a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `description` (str): The new description
- **Returns:** dict with updated file information
- **Use Case:** Add metadata context to files

---

## File Lock & Retention Tools

These tools help you control file access and manage compliance requirements.

### 7. `box_file_lock_tool`
Lock a file to prevent modifications, moves, or renames by other users.
- **Arguments:**
  - `file_id` (str): The ID of the file to lock
  - `lock_expires_at` (str, optional): Lock expiration date in ISO 8601 format
  - `is_download_prevented` (bool, optional): Prevent downloads while locked
- **Returns:** dict with locked file information including lock details
- **Use Case:** Prevent accidental modifications during critical periods

### 8. `box_file_unlock_tool`
Remove a lock from a file.
- **Arguments:**
  - `file_id` (str): The ID of the file to unlock
- **Returns:** dict with unlocked file information
- **Use Case:** Release locked files when modifications are needed

### 9. `box_file_retention_date_set_tool`
Set a retention date for a file (compliance/archival purposes).
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `retention_date` (str): Retention date in ISO 8601 format (e.g., "2025-12-31T23:59:59Z")
- **Returns:** dict with updated file information including retention date
- **Note:** Once set, retention dates cannot be shortened (can only extend)
- **Use Case:** Enforce retention policies for compliance

### 10. `box_file_retention_date_clear_tool`
Clear/remove the retention date from a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with updated file information
- **Use Case:** Remove retention restrictions when no longer needed

---

## File Download Permissions Tools

Control who can download files and under what conditions.

### 11. `box_file_set_download_open_tool`
Allow anyone with file access to download it (overrides role-based restrictions).
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with updated file information
- **Use Case:** Make important files downloadable to all viewers

### 12. `box_file_set_download_company_tool`
Restrict downloads to company users only (viewers and editors cannot download externally).
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with updated file information
- **Use Case:** Keep sensitive content within the organization

### 13. `box_file_set_download_reset_tool`
Reset download permissions to defaults based on collaboration roles.
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with updated file information
- **Use Case:** Remove custom download restrictions

---

## File Tagging Tools

Organize files with tags for easy searching and categorization.

### 14. `box_file_tag_list_tool`
List all tags associated with a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
- **Returns:** dict with list of tags or message if no tags
- **Use Case:** View file categorization

### 15. `box_file_tag_add_tool`
Add a tag to a file (prevents duplicate tags automatically).
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `tag` (str): The tag to add
- **Returns:** dict with updated file information including tags
- **Use Case:** Categorize files for organization

### 16. `box_file_tag_remove_tool`
Remove a tag from a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `tag` (str): The tag to remove
- **Returns:** dict with updated file information
- **Use Case:** Update file categorization

---

## File Thumbnail Tools

Work with file preview thumbnails.

### 17. `box_file_thumbnail_url_tool`
Get the URL for a thumbnail preview image of a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `extension` (str, optional): Image format - 'png' or 'jpg' (default: 'png')
  - `min_height` (int, optional): Minimum height in pixels (32-320)
  - `min_width` (int, optional): Minimum width in pixels (32-320)
  - `max_height` (int, optional): Maximum height in pixels (32-320)
  - `max_width` (int, optional): Maximum width in pixels (32-320)
- **Returns:** dict with thumbnail URL or message if not available
- **Use Case:** Get thumbnail URLs for display in UI

### 18. `box_file_thumbnail_download_tool`
Download the actual thumbnail image of a file.
- **Arguments:**
  - `file_id` (str): The ID of the file
  - `extension` (str, optional): Image format - 'png' or 'jpg' (default: 'png')
  - `min_height` (int, optional): Minimum height in pixels (32-320)
  - `min_width` (int, optional): Minimum width in pixels (32-320)
  - `max_height` (int, optional): Maximum height in pixels (32-320)
  - `max_width` (int, optional): Maximum width in pixels (32-320)
- **Returns:** dict with thumbnail image content in base64 and mime type
- **Use Case:** Retrieve thumbnail images for embedded display

---

## File Transfer Tools

Upload and download file content between local systems and Box.

### 19. `box_file_download_tool`
Download a file from Box and optionally save it locally.
- **Arguments:**
  - `file_id` (str): The ID of the file to download
  - `save_file` (bool, optional): Whether to save the file locally (default: False)
  - `save_path` (str, optional): Local filesystem path to save the file. If not provided but save_file is True, uses a temporary directory
- **Returns:** dict with:
  - `content`: File content (string for text files, base64-encoded for images/binary)
  - `mime_type`: The file's MIME type
  - `path_saved` (optional): Path where file was saved locally
- **Use Case:** Retrieve file content for processing or local storage

### 20. `box_file_upload_tool`
Upload content as a file to Box.
- **Arguments:**
  - `content` (str | bytes): The content to upload (text or binary data)
  - `file_name` (str): The name to give the file in Box
  - `parent_folder_id` (int): The ID of the destination folder (default: root)
- **Returns:** dict with uploaded file information (id, name, etc.)
- **Use Case:** Create new files in Box from content

---

## File Text Extraction Tools

Extract text and structured content from files.

### 21. `box_file_text_extract_tool`
Extract text from a file in Box (returns markdown or plain text).
- **Arguments:**
  - `file_id` (str): The ID of the file to extract text from
- **Returns:** dict with extracted text content
- **Note:** Markdown representation is preferred when available
- **Use Case:** Extract readable text from various file formats (PDF, Word, etc.)

---

## File Operations Quick Reference

| Category | Tools | Purpose |
|----------|-------|---------|
| **Basic Operations** | info, copy, delete, move, rename, description | Manage file metadata and location |
| **Locking & Retention** | lock, unlock, retention_date_set, retention_date_clear | Control access and enforce compliance |
| **Download Control** | set_download_open, set_download_company, set_download_reset | Manage download permissions |
| **Tagging** | tag_list, tag_add, tag_remove | Organize and categorize files |
| **Thumbnails** | thumbnail_url, thumbnail_download | Work with file previews |
| **Transfer** | download, upload | Move content to/from Box |
| **Content** | text_extract | Extract file content |

Refer to [src/tools/box_tools_file.py](src/tools/box_tools_file.py), [src/tools/box_tools_file_transfer.py](src/tools/box_tools_file_transfer.py), and [src/tools/box_tools_file_representation.py](src/tools/box_tools_file_representation.py) for implementation details.
