# Box Tools Groups

This document describes the tools available in the `box_tools_groups` module for group management and queries in Box.

## Available Tools

### 1. `box_groups_search_tool`
Search for groups by name (partial match).
- **Arguments:**
  - `ctx`: Request context
  - `query`: Search query

### 2. `box_groups_list_members_tool`
List all members of a specific group.
- **Arguments:**
  - `ctx`: Request context
  - `group_id`: ID of the group

### 3. `box_groups_list_by_user_tool`
List all groups that a specific user belongs to.
- **Arguments:**
  - `ctx`: Request context
  - `user_id`: ID of the user

---

Refer to `src/tools/box_tools_groups.py` for implementation details.