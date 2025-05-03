[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/box-community-mcp-server-box-badge.png)](https://mseep.ai/app/box-community-mcp-server-box)

# MCP Server Box

## Description

MCP Server Box is a Python project that integrates with the Box API to perform various operations such as file search, text extraction, AI-based querying, and data extraction. It leverages the `box-sdk-gen` library and provides a set of tools to interact with Box files and folders.

The Model Context Protocol (MCP) is a framework designed to standardize the way models interact with various data sources and services. In this project, MCP is used to facilitate seamless integration with the Box API, enabling efficient and scalable operations on Box files and folders. The MCP Server Box project aims to provide a robust and flexible solution for managing and processing Box data using advanced AI and machine learning techniques.

## Tools Implemented

### Box API Tools

#### `box_who_am_i`
Get your current user information and check connection status.
- **Returns:** User information string

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

#### `box_read_tool`
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

### `box_upload_file_tool`
=======
- **Parameters:**
  - `file_id` (str): The ID of the file to be read.
- **Returns:** Text content of the file.

#### `box_ask_ai_tool`
Query Box AI regarding a single file.
- **Parameters:**
  - `file_id` (str): The file identifier.
  - `prompt` (str): Query or instruction for the AI.
- **Returns:** AI response based on the file content.

#### `box_ask_ai_tool_multi_file`
Query Box AI using multiple files.
- **Parameters:**
  - `file_ids` (List[str]): List of file IDs.
  - `prompt` (str): Instruction for the AI based on the aggregate content.
- **Returns:** AI-generated answer considering all files provided.

#### `box_search_folder_by_name`
Locate a folder in Box by its name.
- **Parameters:**
  - `folder_name` (str): Name of the folder.
- **Returns:** Information (name and ID) about matching folders.

#### `box_ai_extract_data`
Extract specific fields from a file using AI.
- **Parameters:**
  - `file_id` (str): ID of the file.
  - `fields` (str): Comma‑separated list of fields to extract.
- **Returns:** Extracted data in JSON string format.

#### `box_list_folder_content_by_folder_id`
List a folder’s content using its ID.
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

To start the MCP server, run the following command:

```sh
uv --directory /Users/anovotny/Desktop/mcp-server-box run src/mcp_server_box.py
```

### Using Claude as the client

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
                    "/Users/anovotny/Desktop/mcp-server-box",
                    "run",
                    "src/mcp_server_box.py"
                ]
            }
        }
    }
    ```

3. Restart Claude if it is running.

### Using Cursor as the client

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
            "/Users/shurrey/local/mcp-server-box",
            "run",
            "src/mcp_server_box.py"
          ]
        }
      }
    }
    ```

6. Save and close the mcp.json file, and restart if necessary.

## Running Tests

The project includes a suite of tests to verify Box API functionality. Before running the tests, update the file and folder IDs in the test files to match those in your Box account.

### Setting Up Tests

1. **Update File and Folder IDs**: 
   - Each test file (in the `tests/` directory) uses hardcoded IDs for Box files and folders.
   - Replace these IDs with valid IDs from your Box account.
2. **File ID References**:
   - For example, in `tests/test_box_api_read.py`, replace `"1728677291168"` with a valid file ID.

### Running Tests

Once you've updated the IDs, you can run the tests using pytest:

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_box_api_file_ops.py

# Run tests with detailed output
pytest -v

# Run tests and show print statements
pytest -v -s
```

### Available Test Suites

- `test_box_auth.py`: Tests authentication functionality.
- `test_box_api_basic.py`: Basic Box API tests.
- `test_box_api_read.py`: Tests file reading capabilities.
- `test_box_api_search.py`: Tests search functionality.
- `test_box_api_ai.py`: Tests AI-based features.
- `test_box_api_file_ops.py`: Tests file upload and download operations.
- Additional tests cover folder operations and Doc Gen features.

## Troubleshooting

If you receive the error `Error: spawn uv ENOENT` on MacOS when running the MCP server with Claude Desktop, you may:
- Remove uv and reinstall it with Homebrew: `brew install uv`
- Or provide the full path to the uv executable in your configuration:
  
  ```sh
  /Users/shurrey/.local/bin/uv --directory /Users/shurrey/local/mcp-server-box run src/mcp_server_box.py
  ```

> [!NOTE]
> Make sure your Box API credentials in `.env` are correctly set.
