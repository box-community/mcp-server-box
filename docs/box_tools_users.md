# Box Tools Users

This document describes the tools available for managing and querying users in Box.

## Available Tools

### 1. `box_users_list_tool`
List all users in the Box account.
- **Arguments:** None
- **Returns:** list[dict] with all users
  - Each user includes: id, name, login (email), status, created_at, modified_at, etc.
- **Use Case:** Get a comprehensive list of all users in the enterprise
- **Performance Note:** May return a large dataset for large enterprises

### 2. `box_users_locate_by_name_tool`
Find a user by their exact full name (case-insensitive).
- **Arguments:**
  - `name` (str): The full name of the user to locate
- **Returns:** dict with user information if found, otherwise error message
  - Returns: id, name, login, email, status, created_at, modified_at
- **Use Case:** Get user ID when you know the exact user name
- **Note:** This is an exact match search; partial names won't match

### 3. `box_users_locate_by_email_tool`
Find a user by their email address (exact match).
- **Arguments:**
  - `email` (str): The email address of the user
- **Returns:** dict with user information if found, otherwise error message
  - Returns: id, name, login, email, status, created_at, modified_at
- **Use Case:** Look up a user by their email address
- **Note:** Email addresses are the most reliable user identifier

### 4. `box_users_search_by_name_or_email_tool`
Search for users by name or email (partial/fuzzy match).
- **Arguments:**
  - `query` (str): Search query (part of name or email)
- **Returns:** list[dict] with matching users
  - Each match includes: id, name, login, email, status, created_at, modified_at
- **Use Case:** Find users when you don't have the exact name or email
- **Examples:**
  - Search by first name: `query: "John"`
  - Search by last name: `query: "Smith"`
  - Search by partial email: `query: "john@example"`

---

## User Information Returned

Each user record includes:
- `id`: Unique Box user ID
- `name`: User's full name
- `login`: User's email/login address
- `email`: User's email address
- `status`: Account status (active, inactive, cannot_delete_login, cannot_delete_edit)
- `created_at`: Account creation timestamp
- `modified_at`: Last modification timestamp
- `role`: User's role (user, admin, coadmin)
- `language`: User's language preference
- `timezone`: User's timezone
- `phone`: User's phone number (if available)
- `address`: User's address (if available)

---

## Usage Tips

1. **Finding Users:**
   - Use `box_users_locate_by_email_tool` for most reliable lookup (email is unique)
   - Use `box_users_locate_by_name_tool` if you know the exact full name
   - Use `box_users_search_by_name_or_email_tool` for fuzzy/partial matching

2. **Performance Considerations:**
   - `box_users_list_tool` returns all users - can be slow for large enterprises
   - Search tools are more efficient for finding specific users
   - Email lookup is fastest when email is available

3. **Use Cases:**
   - **Share files/folders:** Look up user ID to add collaborator
   - **Assign tasks:** Find user ID for task assignment
   - **Collaboration:** Verify user exists before adding to group
   - **Reporting:** List all users for audit purposes

---

## Examples

### Example 1: Find user by email
```
Tool: box_users_locate_by_email_tool
email: "john.smith@example.com"
```
Returns: User ID and full user information

### Example 2: Search for users by partial name
```
Tool: box_users_search_by_name_or_email_tool
query: "john"
```
Returns: All users with "john" in their name or email

### Example 3: Search by partial email
```
Tool: box_users_search_by_name_or_email_tool
query: "john@example"
```
Returns: All users with "john@example" in their email

### Example 4: Get all users
```
Tool: box_users_list_tool
```
Returns: Complete list of all Box users in the enterprise

Refer to [src/tools/box_tools_users.py](src/tools/box_tools_users.py) for implementation details.