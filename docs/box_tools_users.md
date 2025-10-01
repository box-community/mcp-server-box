# Box Tools Users

This document describes the tools available in the `box_tools_users` module for user management and queries in Box.

## Available Tools

### 1. `box_users_list_tool`
List all users in the Box account.
- **Arguments:**
  - `ctx`: Request context

### 2. `box_users_locate_by_name_tool`
Locate a user by their name (exact match).
- **Arguments:**
  - `ctx`: Request context
  - `name`: Name of the user

### 3. `box_users_locate_by_email_tool`
Locate a user by their email address (exact match).
- **Arguments:**
  - `ctx`: Request context
  - `email`: Email address

### 4. `box_users_search_by_name_or_email_tool`
Search for users by name or email (partial match).
- **Arguments:**
  - `ctx`: Request context
  - `query`: Search query

---

Refer to `src/tools/box_tools_users.py` for implementation details.