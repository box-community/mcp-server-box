# Box Tools DocGen

This document describes the tools available in the `box_tools_docgen` module for document generation and template management in Box.

## Available Tools

### Template Management

#### 1. `box_docgen_template_create_tool`
Mark a file as a Box DocGen template.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the file

#### 2. `box_docgen_template_list_tool`
List all Box DocGen templates accessible to the user with pagination support.
- **Arguments:**
  - `ctx`: Request context
  - `marker`: Pagination marker (optional)
  - `limit`: Max items per page (optional)

#### 3. `box_docgen_template_get_by_id_tool`
Retrieve details of a specific DocGen template by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template

#### 4. `box_docgen_template_get_by_name_tool`
Retrieve details of a specific DocGen template by its name.
- **Arguments:**
  - `ctx`: Request context
  - `template_name`: Name of the template

#### 5. `box_docgen_template_delete_tool`
Remove a file as a Box DocGen template.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template

#### 6. `box_docgen_template_list_tags_tool`
List all tags/variables for a DocGen template with version-specific support.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template

#### 7. `box_docgen_template_list_jobs_tool`
List DocGen jobs that used a specific template.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template

### Document Generation

#### 8. `box_docgen_create_batch_tool`
Create a batch of documents from a DocGen template with multiple document generation data sets. Supports PDF and DOCX output.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template
  - `batch_data`: List of data sets for document generation

#### 9. `box_docgen_create_single_file_from_user_input_tool`
Create a single document from a DocGen template using user input data.
- **Arguments:**
  - `ctx`: Request context
  - `template_id`: ID of the template
  - `input_data`: User input data for the template

### Job Management

#### 10. `box_docgen_list_jobs_by_batch_tool`
List DocGen jobs in a specific batch with pagination support.
- **Arguments:**
  - `ctx`: Request context
  - `batch_id`: ID of the batch

#### 11. `box_docgen_get_job_by_id_tool`
Retrieve a DocGen job by its ID.
- **Arguments:**
  - `ctx`: Request context
  - `job_id`: ID of the job

#### 12. `box_docgen_list_jobs_tool`
List all DocGen jobs for the current user with pagination.
- **Arguments:**
  - `ctx`: Request context
  - `marker`: Pagination marker (optional)
  - `limit`: Max items per page (optional)

---

Refer to `src/tools/box_tools_docgen.py` for implementation details.
