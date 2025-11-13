# Box Tools Generic

This document describes the tools available in the `box_tools_generic` module for generic Box API utilities.

## Available Tools

### 1. `get_box_client`
Helper function to get Box client from context. Supports both OAuth and Client Credentials Grant (CCG) authentication modes.
- **Arguments:**
  - `ctx`: Request context

### 2. `box_who_am_i`
Get the current authenticated user's information. Useful for checking connection status.
- **Arguments:**
  - `ctx`: Request context

### 3. `box_authorize_app_tool`
Start the Box application authorization process.
- **Arguments:**
  - None

---

Refer to `src/tools/box_tools_generic.py` for implementation details.
