# Box Tools Metadata

This document describes the tools available in the `box_tools_metadata` module for metadata template and instance management in Box.

## Available Tools

### 1. `box_metadata_template_create_tool`
Create a metadata template.
- **Arguments:**
  - `ctx`: Request context
  - `display_name`: Display name of the template
  - `fields`: List of fields for the template
  - `template_key`: Optional template key

### 2. `box_metadata_get_instance_on_file_tool`
Get a metadata instance on a file.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file
  - `template_key`: Key of the template

...and more tools for setting, updating, and deleting metadata instances. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_metadata.py` for implementation details.