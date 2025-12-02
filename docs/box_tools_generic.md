# Box Tools Generic

This document describes the generic tools available for authentication and connection management with Box.

## Available Tools

### 1. `box_who_am_i`
Get information about the current authenticated user. Useful for verifying connection status and checking authorization.
- **Arguments:** None
- **Returns:** dict with user information
  - `id`: User ID
  - `name`: User name
  - `email`: User email address
  - `login`: User login
  - `status`: User account status
- **Use Case:** Verify Box API connection is working and check current user identity
- **Typical Response:**
  ```json
  {
    "type": "user",
    "id": "123456789",
    "name": "John Doe",
    "login": "john.doe@example.com",
    "created_at": "2023-01-01T00:00:00+00:00",
    "modified_at": "2025-11-20T00:00:00+00:00",
    "language": "en",
    "timezone": "America/New_York",
    "space_amount": 10737418240,
    "space_used": 5000000000,
    "max_upload_size": 5368709120,
    "status": "active"
  }
  ```

### 2. `box_authorize_app_tool`
Start the Box application authorization process (OAuth flow).
- **Arguments:** None
- **Returns:** str with authorization status message
- **Use Case:** Initiate OAuth flow to obtain access tokens when not using Client Credentials Grant (CCG)
- **Note:** This tool is used internally to handle OAuth authentication when not in CCG mode

---

## Helper Functions

### `get_box_client` (Internal Helper)
Helper function to get an authenticated Box client from the request context. Supports both authentication modes:
- **OAuth Mode:** Uses access tokens obtained from Box OAuth flow
- **Client Credentials Grant (CCG):** Uses service account credentials
- **Arguments:**
  - `ctx`: Request context containing Box client configuration
- **Returns:** BoxClient instance ready for API calls

---

## Usage Notes

- The `box_who_am_i` tool is a good starting point to verify your Box connection is working
- Authentication is handled automatically based on your MCP server configuration
- No manual authorization is needed if using Client Credentials Grant (CCG) mode
- For OAuth mode, the authorization flow is handled during server startup

Refer to [src/tools/box_tools_generic.py](src/tools/box_tools_generic.py) and [authentication.md](authentication.md) for implementation details and authentication setup.
