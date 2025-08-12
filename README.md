# Box MCP Server

## Description

The Box MCP Server is a Python project that integrates with the Box API to perform various operations such as file search, text extraction, AI-based querying, and data extraction. It leverages the `box-sdk-gen` library and provides a set of tools to interact with Box files and folders.

The Model Context Protocol (MCP) is a framework designed to standardize the way models interact with various data sources and services. In this project, MCP is used to facilitate seamless integration with the Box API, enabling efficient and scalable operations on Box files and folders. The Box MCP Server project aims to provide a robust and flexible solution for managing and processing Box data using advanced AI and machine learning techniques.

## Tools Implemented

### Box API Tools

#### `box_who_am_i`
Get your current user information and check connection status.
- **Returns:** User information dictionary

#### `box_authorize_app_tool`
Start the Box application authorization process.
- **Returns:** Authorization status message

#### `box_search_tool`
Search for files in Box.
- **Parameters:**
  - `query` (str): The query to search for.
  - `file_extensions` (List[str], optional): File extensions to filter results.
  - `where_to_look_for_query` (List[str], optional): Locations to search (e.g. NAME, DESCRIPTION, FILE_CONTENT, COMMENTS, TAG).
  - `ancestor_folder_ids` (List[str], optional): List of folder IDs in which to search.
- **Returns:** The search results as a newline‑separated list of file names and IDs.

### `box_read_tool`
Read the text content of a Box file.

**Parameters:**
- `file_id` (str): ID of the file to read

**Returns:** File content

### `box_ask_ai_tool`
Ask Box AI about a file.

**Parameters:**
- `file_id` (str): ID of the file
- `prompt` (str): Question for the AI

**Returns:** AI response

### `box_hubs_ask_ai_tool`
Ask Box AI about a hub. There is currently no way via API to discover a hub ID, so you must know the ID to use this tool. We will fix this in the future.

**Parameters:**
- `hubs_id` (str): ID of the hub
- `prompt` (str): Question for the AI

**Returns:** AI response

### `box_search_folder_by_name`
Locate a folder by name.

**Parameters:**
- `folder_name` (str): Name of the folder

**Returns:** Folder ID

### `box_ai_extract_data`
Extract data from a file using AI.

**Parameters:**
- `file_id` (str): ID of the file
- `fields` (str): Fields to extract

**Returns:** Extracted data in JSON format

### `box_list_folder_content_by_folder_id`
List folder contents.

**Parameters:**
- `folder_id` (str): ID of the folder
- `is_recursive` (bool): Whether to list recursively

**Returns:** Folder content in JSON format with id, name, type, and description

### `box_manage_folder_tool`
Create, update, or delete folders in Box.

**Parameters:**
- `action` (str): Action to perform: "create", "delete", or "update"
- `folder_id` (str, optional): ID of the folder (required for delete/update)
- `name` (str, optional): Folder name (required for create, optional for update)
- `parent_id` (str, optional): Parent folder ID (required for create, optional for update)
- `description` (str, optional): Folder description (optional for update)
- `recursive` (bool, optional): Whether to delete recursively (optional for delete)

**Returns:** Status message with folder details

#### `box_search_folder_by_name_tool`
Locate a folder in Box by its name.
- **Parameters:**
  - `folder_name` (str): Name of the folder.
- **Returns:** Information (name and ID) about matching folders.

### Box AI Tools

#### `box_ai_ask_file_single_tool`
Query Box AI regarding a single file.
- **Parameters:**
  - `file_id` (str): The file identifier.
  - `prompt` (str): Query or instruction for the AI.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** AI response based on the file content.

#### `box_ai_ask_file_multi_tool`
Query Box AI using multiple files.
- **Parameters:**
  - `file_ids` (List[str]): List of file IDs.
  - `prompt` (str): Instruction for the AI based on the aggregate content.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** AI-generated answer considering all files provided.

#### `box_ai_ask_hub_tool`
Ask Box AI about a hub.
- **Parameters:**
  - `hubs_id` (str): ID of the hub.
  - `prompt` (str): Question for the AI.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** AI response based on the hub content.

#### `box_ai_extract_freeform_tool`
Extract data from files using AI with a freeform prompt.
- **Parameters:**
  - `file_ids` (List[str]): The IDs of the files to read.
  - `prompt` (str): The freeform prompt to guide the AI extraction.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** Extracted data in JSON format.

#### `box_ai_extract_structured_using_fields_tool`
Extract structured data from files using AI with specified fields.
- **Parameters:**
  - `file_ids` (List[str]): The IDs of the files to read.
  - `fields` (List[dict]): The fields to extract from the files.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** Extracted structured data in JSON format.

#### `box_ai_extract_structured_using_template_tool`
Extract structured data from files using AI with a specified template.
- **Parameters:**
  - `file_ids` (List[str]): The IDs of the files to read.
  - `template_key` (str): The ID of the template to use for extraction.
  - `ai_agent_id` (str, optional): The ID of the AI agent to use.
- **Returns:** Extracted structured data in JSON format.

#### `box_ai_extract_structured_enhanced_using_fields_tool`
Extract structured data from files using AI with enhanced processing and specified fields.
- **Parameters:**
  - `file_ids` (List[str]): The IDs of the files to read.
  - `fields` (List[dict]): The fields to extract from the files.
- **Returns:** Enhanced extracted structured data in JSON format.

#### `box_ai_extract_structured_enhanced_using_template_tool`
Extract structured data from files using AI with enhanced processing and a template.
- **Parameters:**
  - `file_ids` (List[str]): The IDs of the files to read.
  - `template_key` (str): The ID of the template to use for extraction.
- **Returns:** Enhanced extracted structured data in JSON format.

### Box File Tools

#### `box_read_tool`
Read the text content of a Box file.
- **Parameters:**
  - `file_id` (str): The ID of the file to be read.
- **Returns:** Text content of the file.

#### `box_list_folder_content_by_folder_id`
List a folder's content using its ID.
- **Parameters:**
  - `folder_id` (str): Folder ID.
  - `is_recursive` (bool, optional): Whether to list the content recursively.
- **Returns:** Folder contents as a JSON string including id, name, type, and description.

#### `box_manage_folder_tool`
Create, update, or delete a folder in Box.
- **Parameters:**
  - `action` (str): Action to perform: "create", "delete", or "update".
  - `folder_id` (str, optional): Folder ID (required for delete and update).
  - `name` (str, optional): Folder name (required for create, optional for update).
  - `parent_id` (str, optional): Parent folder ID (defaults to "0" for root).
  - `description` (str, optional): Description for the folder (for update).
  - `recursive` (bool, optional): For recursive delete.
- **Returns:** Status message with folder details.

#### `box_upload_file_from_path_tool`
Upload a file to Box from a local filesystem path.
- **Parameters:**
  - `file_path` (str): Local file path.
  - `folder_id` (str, optional): Destination folder ID (defaults to "0").
  - `new_file_name` (str, optional): New file name (if not provided, uses the original file name).
- **Returns:** Details about the uploaded file (ID and name) or an error message.

#### `box_upload_file_from_content_tool`
Upload content as a file to Box.
- **Parameters:**
  - `content` (str | bytes): Content to upload (text or binary).
  - `file_name` (str): The name to assign the file.
  - `folder_id` (str, optional): Destination folder ID (defaults to "0").
  - `is_base64` (bool, optional): Indicates if the provided content is base64 encoded.
- **Returns:** Upload success message with file ID and name.

#### `box_download_file_tool`
Download a file from Box.
- **Parameters:**
  - `file_id` (str): The ID of the file to download.
  - `save_file` (bool, optional): Whether to save the file locally.
  - `save_path` (str, optional): The local path where the file should be saved.
- **Returns:** For text files, returns the content; for images, returns base64‑encoded data; for other types, an error or save‑confirmation message.

### Box Metadata Tools

#### `box_metadata_template_create_tool`
Create a metadata template.
- **Parameters:**
  - `display_name` (str): The display name of the metadata template.
  - `fields` (List[Dict]): A list of fields to include in the template.
  - `template_key` (str, optional): An optional key for the metadata template.
- **Returns:** The created metadata template.

#### `box_metadata_template_get_by_key_tool`
Retrieve a metadata template by its key.
- **Parameters:**
  - `template_name` (str): The key of the metadata template to retrieve.
- **Returns:** The metadata template associated with the provided key.

#### `box_metadata_template_get_by_name_tool`
Retrieve a metadata template by its name.
- **Parameters:**
  - `template_name` (str): The name of the metadata template to retrieve.
- **Returns:** The metadata template associated with the provided name.

#### `box_metadata_set_instance_on_file_tool`
Set a metadata instance on a file.
- **Parameters:**
  - `template_key` (str): The key of the metadata template.
  - `file_id` (str): The ID of the file to set the metadata on.
  - `metadata` (dict): The metadata to set.
- **Returns:** The response from the Box API after setting the metadata.

#### `box_metadata_get_instance_on_file_tool`
Get a metadata instance on a file.
- **Parameters:**
  - `file_id` (str): The ID of the file to get the metadata from.
  - `template_key` (str): The key of the metadata template.
- **Returns:** The metadata instance associated with the file.

#### `box_metadata_update_instance_on_file_tool`
Update a metadata instance on a file.
- **Parameters:**
  - `file_id` (str): The ID of the file to update the metadata on.
  - `template_key` (str): The key of the metadata template.
  - `metadata` (dict): The metadata to update.
  - `remove_non_included_data` (bool, optional): If True, remove data from fields not included in the metadata.
- **Returns:** The response from the Box API after updating the metadata.

#### `box_metadata_delete_instance_on_file_tool`
Delete a metadata instance on a file.
- **Parameters:**
  - `file_id` (str): The ID of the file to delete the metadata from.
  - `template_key` (str): The key of the metadata template.
- **Returns:** The response from the Box API after deleting the metadata.

### Box Doc Gen Tools

#### `box_docgen_create_batch_tool`
Generate documents using a Box Doc Gen template and a local JSON file.
- **Parameters:**
  - `file_id` (str): Template file ID.
  - `destination_folder_id` (str): Folder ID where generated documents should be stored.
  - `user_input_file_path` (str): Path to a JSON file with input data.
  - `output_type` (str, optional): Output format (default is "pdf").
- **Returns:** The result of the document generation batch as a JSON string.

#### `box_docgen_get_job_tool`
Fetch a single Doc Gen job by its ID.
- **Parameters:**
  - `job_id` (str): The job identifier.
- **Returns:** Job details in a JSON‑formatted string.

#### `box_docgen_list_jobs_tool`
List all Doc Gen jobs associated with the current user.
- **Parameters:**
  - `marker` (str | None, optional): Pagination marker.
  - `limit` (int | None, optional): Maximum number of jobs to return.
- **Returns:** Paginated list of jobs in pretty‑printed JSON.

#### `box_docgen_list_jobs_by_batch_tool`
List Doc Gen jobs belonging to a specific batch.
- **Parameters:**
  - `batch_id` (str): The batch identifier.
  - `marker` (str | None, optional): Pagination marker.
  - `limit` (int | None, optional): Maximum number of jobs to return.
- **Returns:** Batch jobs details as JSON.

#### `box_docgen_template_create_tool`
Mark a file as a Box Doc Gen template.
- **Parameters:**
  - `file_id` (str): File ID to mark as a template.
- **Returns:** Template details after marking.

#### `box_docgen_template_list_tool`
List all available Box Doc Gen templates.
- **Parameters:**
  - `marker` (str | None, optional): Pagination marker.
  - `limit` (int | None, optional): Maximum number of templates to list.
- **Returns:** List of templates in JSON format.

#### `box_docgen_template_delete_tool`
Remove the Doc Gen template marking from a file.
- **Parameters:**
  - `template_id` (str): The template identifier.
- **Returns:** Confirmation of deletion as JSON.

#### `box_docgen_template_get_by_id_tool`
Retrieve details of a specific Doc Gen template.
- **Parameters:**
  - `template_id` (str): The template identifier.
- **Returns:** Template details as JSON.

#### `box_docgen_template_list_tags_tool`
List all tags associated with a Box Doc Gen template.
- **Parameters:**
  - `template_id` (str): The template ID.
  - `template_version_id` (str | None, optional): Specific version ID.
  - `marker` (str | None, optional): Pagination marker.
  - `limit` (int | None, optional): Maximum number of tags to return.
- **Returns:** List of tags in JSON format.

#### `box_docgen_template_list_jobs_tool`
List all Doc Gen jobs that used a specific template.
- **Parameters:**
  - `template_id` (str): The template identifier.
  - `marker` (str | None, optional): Pagination marker.
  - `limit` (int | None, optional): Maximum number of jobs to list.
- **Returns:** Job details for the template as a JSON string.

### Box Share Link Tools

#### box_create_share_link_tool
Create a shared link for a Box file with customizable access controls.

**Parameters:**
- `file_id` (str, required): The ID of the file to share
- `access` (str, optional): Access level - 'open', 'company', or 'collaborators' (default: "open")
- `password` (str, optional): Password to protect the link
- `unshared_at` (str, optional): Expiration date in ISO-8601 format
- `vanity_name` (str, optional): Custom vanity name for the shared link
- `can_download` (bool, optional): Whether the file can be downloaded (default: True)

**Returns:**
JSON string containing the share link details including URL, download URL, and access information.

#### box_get_shared_link_tool
Retrieve an existing shared link for a Box file.

**Parameters:**
- `file_id` (str, required): The ID of the file

**Returns:**
JSON string with existing share link information or a message if no link exists.

#### box_remove_shared_link_tool
Remove a shared link from a Box file.

**Parameters:**
- `file_id` (str, required): The ID of the file

**Returns:**
JSON string with confirmation message.

## Requirements

- Python 3.13 or higher
- Box API credentials (Client ID, Client Secret, etc.)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/box-community/mcp-server-box.git
    cd mcp-server-box
    ```

2. Install `uv` if not installed yet:

    2.1 MacOS+Linux

    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    2.2 Windows

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    
3. Create and set up our project:

    3.1 MacOS+Linux

    ```sh
    # Create virtual environment and activate it
    uv venv
    source .venv/bin/activate

    # Lock the dependencies
    uv lock
    ```

    3.2 Windows

    ```sh
    # Create virtual environment and activate it
    uv venv
    .venv\Scripts\activate

    # Lock the dependencies
    uv lock
    ```

4. Create a `.env` file in the root directory and add your Box API credentials:

    ```.env
    BOX_CLIENT_ID=your_client_id
    BOX_CLIENT_SECRET=your_client_secret
    ```

## Usage

### Running the MCP Server

The MCP server supports four transport methods: **stdio** (default), **SSE** (Server-Sent Events), **HTTP** (StreamableHttp), and **FastAPI**.

#### Running with stdio transport (default)

```sh
uv --directory /path/to/mcp-server-box run src/mcp_server_box.py
```



### Using Claude as the client

#### For stdio transport (recommended for Claude Desktop)

1. Edit your `claude_desktop_config.json`:

    ```sh
    code ~/Library/Application\ Support/Claude/claude_desktop_config.json
    ```

2. Add the configuration:

    ```json
    {
        "mcpServers": {
            "mcp-server-box": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/path/to/mcp-server-box",
                    "run",
                    "src/mcp_server_box.py"
                ]
            }
        }
    }
    ```

3. Restart Claude if it is running.


### Using Cursor as the client

#### For stdio transport

1. Open your IDE with Cursor.
2. In settings, select `Cursor settings`.
3. In the left nav, select `MCP`.
4. In the top-left, click `Add new global MCP server`.
5. Paste the following JSON (update for your local values):

    ```json
    {
      "mcpServers": {
        "box": {
          "command": "uv",
          "args": [
            "--directory",
            "/path/to/mcp-server-box",
            "run",
            "src/mcp_server_box.py"
          ]
        }
      }
    }
    ```

6. Save and close the mcp.json file, and restart if necessary.


## Running Tests

The project includes comprehensive test suites for both unit tests and integration tests to verify Box API functionality.

### Test Structure

The project includes two types of tests:

1. **Unit Tests** - Mock-based tests that don't require Box API access:
   - `test_box_tools_ai.py` - Tests for AI functionality tools
   - `test_box_tools_generic.py` - Tests for generic Box operations
   - `test_box_tools_metadata.py` - Tests for metadata operations
   - `test_box_tools_search.py` - Tests for search functionality
   - `test_server_context.py` - Tests for server context management
   - `test_mcp_server_box.py` - Tests for MCP server functionality

2. **Integration Tests** - Tests that require actual Box API access (with `_orig` suffix):
   - `test_box_tools_files_orig.py`
   - `test_box_tools_metadata_orig.py`
   - `test_box_tools_search_orig.py`

### Running Unit Tests

Unit tests use mocks and don't require Box API credentials:

```bash
# Run all unit tests
pytest tests/test_box_tools_*.py tests/test_server_context.py tests/test_mcp_server_box.py

# Run specific unit test files
pytest tests/test_box_tools_ai.py
pytest tests/test_box_tools_generic.py
pytest tests/test_box_tools_metadata.py

# Run with coverage
pytest --cov=src tests/
```

### Running Integration Tests

Integration tests require Box API credentials and valid file/folder IDs in your Box account:

1. **Set up Box API credentials** in your `.env` file
2. **Update File and Folder IDs**: 
   - Each integration test file (ending with `_orig.py`) uses hardcoded IDs for Box files and folders
   - Replace these IDs with valid IDs from your Box account
3. **File ID References**:
   - For example, in `tests/test_box_tools_files_orig.py`, replace `"1728677291168"` with a valid file ID

```bash
# Run integration tests
pytest tests/test_*_orig.py

# Run specific integration test
pytest tests/test_box_tools_files_orig.py

# Run all tests (unit + integration)
pytest

# Run with detailed output
pytest -v

# Run with print statements
pytest -v -s
```

### Test Dependencies

The test suite uses:
- `pytest` - Test framework
- `pytest-asyncio` - For async test support  
- `pytest-cov` - For coverage reporting
- `unittest.mock` - For mocking external dependencies


## Troubleshooting

If you receive the error `Error: spawn uv ENOENT` on MacOS when running the MCP server with Claude Desktop, you may:
- Remove uv and reinstall it with Homebrew: `brew install uv`
- Or provide the full path to the uv executable in your configuration:
  
  ```sh
  /Users/shurrey/.local/bin/uv --directory /Users/shurrey/local/mcp-server-box run src/mcp_server_box.py
  ```

> [!NOTE]
> Make sure your Box API credentials in `.env` are correctly set.
