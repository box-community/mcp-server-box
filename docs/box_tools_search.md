# Box Tools Search

This document describes the search tools available for finding files and folders in Box.

## Available Tools

### 1. `box_search_tool`
Search for files and folders in Box using a query with optional filtering.
- **Arguments:**
  - `query` (str): Search query string (searches file names, descriptions, and content)
  - `file_extensions` (list[str], optional): Filter by file extensions (e.g., ["pdf", "docx"])
  - `where_to_look_for_query` (list[str], optional): Where to search - possible values:
    - `NAME`: Search in file/folder names
    - `DESCRIPTION`: Search in descriptions
    - `FILE_CONTENT`: Search in file content
    - `COMMENTS`: Search in file comments
    - `TAG`: Search in tags
  - `ancestor_folder_ids` (list[str], optional): Limit search to specific folders
- **Returns:** list[dict] with search results
  - Each result includes: id, name, type (file/folder), created_at, modified_at, etc.
- **Use Cases:**
  - Find files by name: `query: "contract"` with `where_to_look_for_query: ["NAME"]`
  - Find PDFs: `query: "invoice"` with `file_extensions: ["pdf"]`
  - Search content in specific folder: `query: "project deadline"` with `ancestor_folder_ids: ["12345"]`
  - Full-text search: `query: "budget 2025"` with `where_to_look_for_query: ["FILE_CONTENT"]`

### 2. `box_search_folder_by_name_tool`
Locate a folder in Box by its exact or partial name.
- **Arguments:**
  - `folder_name` (str): The name of the folder to find
- **Returns:** list[dict] with matching folders
  - Each result includes: id, name, type, path, parent_id, etc.
- **Use Cases:**
  - Find a folder by name: `folder_name: "Project A"`
  - Locate a team folder: `folder_name: "Marketing Team"`
  - Search for shared folders: `folder_name: "Shared Workspace"`

---

## Search Tips

1. **Exact Match vs. Partial Match:**
   - `box_search_tool` supports partial matching by default
   - `box_search_folder_by_name_tool` also supports partial matching
   - Use specific search terms for better results

2. **Combining Filters:**
   - Combine multiple filters for more precise searches
   - Example: Search for PDFs in a specific folder
   - Example: Search for files modified in the last month with specific tag

3. **Content Search:**
   - To search within file content, use `where_to_look_for_query: ["FILE_CONTENT"]`
   - This is useful for finding documents containing specific text

4. **Performance:**
   - More specific queries return results faster
   - Limiting searches to specific folders improves performance
   - Using file extensions filter reduces result set

---

## Examples

### Example 1: Search for contracts
```
Tool: box_search_tool
query: "contract"
where_to_look_for_query: ["NAME", "DESCRIPTION"]
```

### Example 2: Find all PDF files
```
Tool: box_search_tool
query: "*"
file_extensions: ["pdf"]
```

### Example 3: Search in specific folder
```
Tool: box_search_tool
query: "budget"
ancestor_folder_ids: ["12345"]
where_to_look_for_query: ["FILE_CONTENT"]
```

### Example 4: Find a team folder
```
Tool: box_search_folder_by_name_tool
folder_name: "Finance Team"
```

Refer to [src/tools/box_tools_search.py](src/tools/box_tools_search.py) for implementation details.