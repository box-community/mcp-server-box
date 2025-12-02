# Box Tools Groups

This document describes the tools available for managing and querying groups in Box.

## Available Tools

### 1. `box_groups_search_tool`
Search for groups by name (partial/fuzzy match).
- **Arguments:**
  - `query` (str): Search query string (part of group name)
- **Returns:** list[dict] with matching groups
  - Each group includes: id, name, description, created_at, updated_at, etc.
- **Use Case:** Find a group by partial name
- **Examples:**
  - Search for department: `query: "Finance"`
  - Search for team: `query: "Marketing"`
  - Search for project: `query: "Project A"`

### 2. `box_groups_list_members_tool`
List all members of a specific group.
- **Arguments:**
  - `group_id` (str): The ID of the group
- **Returns:** list[dict] with group members
  - Each member includes: id, name, login (email), status, role, etc.
- **Use Case:** View who is in a group
- **Typical Use Cases:**
  - Verify group membership
  - See all users in a department or team
  - Check group composition

### 3. `box_groups_list_by_user_tool`
List all groups that a specific user belongs to.
- **Arguments:**
  - `user_id` (str): The ID of the user
- **Returns:** list[dict] with groups the user is a member of
  - Each group includes: id, name, description, created_at, updated_at, etc.
- **Use Case:** See all groups a user is part of
- **Typical Use Cases:**
  - Check user group memberships
  - See which teams/departments a user belongs to
  - Audit user access

---

## Group Information Returned

Each group record includes:
- `id`: Unique Box group ID
- `name`: Group name
- `description`: Group description (if available)
- `created_at`: Group creation timestamp
- `updated_at`: Last modification timestamp
- `provenance`: Group type (e.g., "manual" for manually created groups)

---

## Member Information Returned

Each member record includes:
- `id`: User ID
- `name`: User's full name
- `login`: User's email/login address
- `status`: User status (active, inactive, etc.)
- `created_at`: User creation timestamp
- `modified_at`: Last modification timestamp

---

## Usage Tips

1. **Finding Groups:**
   - Use `box_groups_search_tool` to find groups by partial name
   - Groups are useful for bulk collaborations and access control

2. **Membership Management:**
   - Use `box_groups_list_members_tool` to see who's in a group
   - Use `box_groups_list_by_user_tool` to see what groups a user belongs to
   - Combine both to understand group structure and user assignments

3. **Common Patterns:**
   - **Department Groups:** Groups organized by department (Finance, HR, Sales)
   - **Project Groups:** Groups organized by project
   - **Team Groups:** Groups organized by team or function
   - **Role-based Groups:** Groups based on job roles or responsibilities

---

## Examples

### Example 1: Find a group by name
```
Tool: box_groups_search_tool
query: "Finance"
```
Returns: All groups with "Finance" in their name

### Example 2: View group members
```
Tool: box_groups_list_members_tool
group_id: "123456"
```
Returns: All users who are members of group 123456

### Example 3: See user's group memberships
```
Tool: box_groups_list_by_user_tool
user_id: "987654"
```
Returns: All groups that user 987654 belongs to

### Example 4: Find team members in a department
```
// First, find the department group
Tool: box_groups_search_tool
query: "Marketing Team"

// Then, list all members of that group
Tool: box_groups_list_members_tool
group_id: [result from previous search]
```
Returns: All members of the Marketing Team group

---

## Workflow Examples

### Scenario: Share a file with all team members
1. Search for the group: `box_groups_search_tool` with team name
2. Get group ID from results
3. Use the group ID in collaboration tools to share with all members at once

### Scenario: Audit user access
1. Get user's groups: `box_groups_list_by_user_tool` with user ID
2. For each group, see members: `box_groups_list_members_tool`
3. Review which users share access through group memberships

Refer to [src/tools/box_tools_groups.py](src/tools/box_tools_groups.py) for implementation details.