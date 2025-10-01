# Box Tools DocGen

This document describes the tools available in the `box_tools_docgen` module for document generation and template management in Box.

## Available Tools

### 1. `box_docgen_template_create_tool`
Mark a file as a Box Doc Gen template.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file

### 2. `box_docgen_template_list_tool`
List all Box Doc Gen templates accessible to the user.
- **Arguments:**
  - `ctx`: Request context
  - `marker`: Pagination marker (optional)
  - `limit`: Max items per page (optional)

### 3. `box_docgen_template_get_by_id_tool`
Get a template by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template

...and more tools for job management, batch creation, and template operations. Refer to the source for additional functions.

---

Refer to `src/tools/box_tools_docgen.py` for implementation details.