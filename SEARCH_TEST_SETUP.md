# Box Search Test Setup Guide (JWT `config.json` Method)

This guide provides the definitive instructions to set up and use the Box search functionality using the standard, non-interactive JWT authentication with a `config.json` file. This is the most reliable method for server-to-server applications.

## Final Setup Steps

### 1. Box App Configuration (One-time only)
In the [Box Developer Console](https://developer.box.com/console):
- **Go to your "Custom App"**.
- Select the **"Configuration"** tab.
- **Authentication Method:** Ensure **"Server Authentication (with JWT)"** is selected.
- **Application Scopes:** Check `Read and write all files and folders stored in Box`.
- **Advanced Features:** Check `Make API calls using the as-user header`.
- **Add and Manage Public Keys:** Click **"Generate a Public/Private Keypair"**. This action will do two things:
    1.  Add a Public Key to your application.
    2.  Trigger the download of a `config.json` file.
- **Save the `config.json` file** in the root of this project directory.
- **Save all changes** to your Box application configuration.

### 2. Authorize the App in the Admin Console
- Go to your organization's Box **Admin Console**.
- Navigate to **Apps -> Custom Apps Manager**.
- Find your application by its Client ID.
- **Authorize the application**. It must be explicitly enabled by an admin.

### 3. Project Dependencies
- **You no longer need a `.env` file for authentication.**
- Ensure you have the required Python packages installed:
  ```bash
  uv sync
  ```

## Running the Search Test

With the `config.json` file in place, you can run searches directly from the command line. The script will automatically use the credentials and user ID specified within that file.

```bash
# Run a search
./run_search_test "find me estates with death certificates"
```

## Troubleshooting

- **`config.json not found`**: Make sure the file you downloaded from the Box Dev Console is in the project root and is named exactly `config.json`.
- **`"error":"key_invalid"`**: The public key generated in step 1 is not approved or active in the Box Dev Console. Re-generate it or check its status.
- **`"message":"invalid_grant"` or Access Denied errors**:
  1. The app has not been authorized in the **Admin Console**. This is the most common cause.
  2. The user specified in your `config.json` file (`boxSubjectID`) does not have sufficient permissions or their account is inactive.
  3. Your application scopes are insufficient.

### No Results Found
- Check that files exist in your Box account
- Verify that files have descriptions, tags, or comments
- Try broader search terms
- Make sure your Box API credentials are correct

### Search Performance
- Box search may take a few seconds for large accounts
- File content search depends on Box's indexing (some file types may not be searchable)
- Consider searching in specific folders to narrow results

## Advanced Usage

### Custom Search Parameters

You can modify `run_search_test.py` to add custom search parameters:

```python
# Search in specific folders only
search_params['ancestor_folder_ids'] = ['folder_id_1', 'folder_id_2']

# Search only specific file types
search_params['file_extensions'] = ['pdf', 'docx']

# Search only in specific metadata fields
search_params['where_to_look_for_query'] = ['NAME', 'DESCRIPTION']
```

### Integration with Other Tools

Once you find files, you can use their IDs with other Box tools:

```python
# Read file content
box_read_tool(file_id)

# Ask AI about the file
box_ask_ai_tool(file_id, "What are the key points?")

# Extract specific data
box_ai_extract_data(file_id, "contract date, parties involved")
```

## Next Steps

1. **Set up your Box account** with test files that have descriptions, tags, and comments
2. **Run the search tests** to verify functionality
3. **Customize the search queries** to match your specific use cases
4. **Integrate with your workflows** using the file IDs returned by searches 