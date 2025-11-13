# Box Tools Metadata

This document describes the tools available in the `box_tools_metadata` module for metadata template and instance management in Box.

## Available Tools

### Metadata Template Management

#### 1. `box_metadata_template_create_tool`
Create a new metadata template definition in Box with custom fields (string, date, enum, multiSelect types).
- **Arguments:**
  - `ctx`: Request context
  - `display_name`: Display name of the template
  - `fields`: List of field definitions for the template
  - `template_key`: Optional template key

#### 2. `box_metadata_template_list_tool`
List all metadata templates in Box.
- **Arguments:**
  - `ctx`: Request context

#### 3. `box_metadata_template_get_by_key_tool`
Retrieve a metadata template by its key.
- **Arguments:**
  - `ctx`: Request context
  - `template_key`: Key of the template to retrieve

#### 4. `box_metadata_template_get_by_name_tool`
Retrieve a metadata template by its name.
- **Arguments:**
  - `ctx`: Request context
  - `template_name`: Name of the template to retrieve

### Metadata Instance Management

#### 5. `box_metadata_set_instance_on_file_tool`
Set a metadata template instance on a specific file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `template_key`: Key of the template
  - `metadata_values`: Dictionary of metadata field values

#### 6. `box_metadata_get_instance_on_file_tool`
Get the metadata template instance associated with a specific file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `template_key`: Key of the template

#### 7. `box_metadata_update_instance_on_file_tool`
Update the metadata template instance on a file with optional removal of non-included data.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `template_key`: Key of the template
  - `metadata_values`: Dictionary of metadata field values to update

#### 8. `box_metadata_delete_instance_on_file_tool`
Delete the metadata template instance associated with a specific file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `template_key`: Key of the template

---

Refer to `src/tools/box_tools_metadata.py` for implementation details.
