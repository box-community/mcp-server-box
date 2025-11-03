# Authentication Guide

The Box MCP Server supports multiple authentication configurations to accommodate different deployment scenarios and security requirements. Authentication is controlled by two independent parameters:

- **`--mcp-auth-type`**: Controls authentication between the MCP client and the MCP server
- **`--box-auth-type`**: Controls authentication between the MCP server and the Box API

## Command Line Options

```bash
usage: mcp_server_box.py [-h] [--transport {stdio,sse,http}] [--host HOST] [--port PORT]
                         [--mcp-auth-type {oauth,token,none}]
                         [--box-auth-type {oauth,ccg,jwt,mcp_client}]

options:
  --transport {stdio,sse,http}
                        Transport type (default: stdio)
  --host HOST           Host for SSE/HTTP transport (default: localhost)
  --port PORT           Port for SSE/HTTP transport (default: 8005)
  --mcp-auth-type {oauth,token,none}
                        Authentication type for MCP server (default: token)
  --box-auth-type {oauth,ccg,jwt,mcp_client}
                        Authentication type for Box API (default: oauth)
```

## MCP Authentication Types

### `oauth`
- Uses the MCP client OAuth protocol
- Implements partial Dynamic Client Registration
- Can accept specific client ID and client secret credentials configured on the MCP client
- **Must be used with `--box-auth-type=mcp_client`**
- Box authentication is delegated to the MCP client

### `token`
- API key style authentication for the MCP server
- Configure an access token that the MCP server validates against incoming requests
- Independent of Box API authentication
- **Requires server-side Box authentication** (oauth, ccg, or jwt)
- **Cannot be used with `--box-auth-type=mcp_client`**

### `none`
- No authentication validation between MCP client and server
- Assumes all requests from the MCP client are valid
- Independent of Box API authentication
- **Most flexible** - works with all Box authentication types
- **Note**: `stdio` transport forces the usage of `none`

## Box Authentication Types

The Box API always requires authentication. The MCP server supports multiple Box authentication methods:

### `oauth`
- Standard Box OAuth 2.0 user authentication
- Opens browser for user authorization
- Requires a Box Custom App with OAuth 2.0 enabled
- Authenticates as the user who authorizes the application
- Maintains user's Box security context
- Requires Box OAuth client ID and client secret configuration

### `ccg` (Client Credentials Grant)
- Server-side authentication using Client Credentials Grant
- Requires a Box Custom App with CCG enabled
- Authenticates as a Service Account or specific user
- Requires Box admin to enable the application
- Requires Box client ID, client secret, and enterprise ID
- Ideal for service account scenarios

### `jwt` (JSON Web Token)
- Server-side authentication using JWT
- Requires a Box JWT App with public/private key pair
- Uses the JSON config file downloaded from Box Developer Console
- Authenticates as the Service Account
- Requires Box admin to enable the application
- Can act on behalf of other users if configured

### `mcp_client`
- Delegates Box authentication to the MCP client
- The MCP server creates a BoxClient object using credentials provided by the client
- **With `mcp-auth-type=oauth`**: MCP client configures Box OAuth during the MCP OAuth flow
- **With `mcp-auth-type=none`**: MCP client must send a valid Box API Bearer token in the Authorization header
- Useful when the MCP client handles Box authorization (developer token, OAuth, CCG, or JWT)

## Dynamic Client Registration (Partial Implementation)

When using `--mcp-auth-type=oauth` with `--box-auth-type=mcp_client`, the MCP server implements a **partial version** of Dynamic Client Registration to enable the MCP OAuth flow with Box authentication.

### Why Partial Implementation?

**Box API does not natively support Dynamic Client Registration**. To work around this limitation, the MCP server simulates the registration endpoint internally.

### How It Works

1. **Registration Endpoint**: The MCP server exposes a registration endpoint that the MCP client calls during the OAuth flow
2. **Static Credentials**: The endpoint always returns the same `client_id` and `client_secret` configured in your `.env` file (e.g., `.env.oauth`)
3. **Pre-configured Box App**: You must create and configure a Box OAuth application in advance through the [Box Developer Console](https://app.box.com/developers/console)

### Important Limitations

#### Callback URLs Must Be Pre-Registered

**Dynamic callback URLs are NOT supported**. You must manually pre-register all callback/redirect URIs in your Box application configuration:

1. Go to the [Box Developer Console](https://app.box.com/developers/console)
2. Select your OAuth application
3. Navigate to "Configuration" → "OAuth 2.0 Redirect URI"
4. Add all callback URLs that will be used. Common examples include:
   - `https://claude.ai/api/mcp/auth_callback` (for Claude)
   - `https://claude.com/api/mcp/auth_callback` (for Claude future use)
   - `http://localhost:6274/oauth/callback` (for MCP Inspector)
   - `http://localhost:6274/oauth/callback/debug` (for MCP Inspector)
   - `https://vscode.dev/redirect` (for VS Code)
5. Save the configuration

**Note**: If the MCP client attempts to use a callback URL that is not pre-registered in the Box application, the OAuth flow will fail with an error from Box.

### Configuration Requirements

For this to work, your `.env` file must contain:

```bash
BOX_CLIENT_ID = your_box_client_id
BOX_CLIENT_SECRET = your_box_client_secret
BOX_REDIRECT_URL = http://localhost:8000/callback  # Must match Box app configuration

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

The `BOX_REDIRECT_URL` must be one of the redirect URIs configured in your Box application.

## Compatibility Matrix

| mcp-auth-type | box-auth-type | Valid | Notes |
|---------------|---------------|-------|-------|
| **oauth** | oauth | ❌ | Not supported |
| **oauth** | ccg | ❌ | Not supported |
| **oauth** | jwt | ❌ | Not supported |
| **oauth** | **mcp_client** | ✅ | **Recommended for Claude Desktop**. Supports sending client ID and client secret configurations in MCP client. Partial support of Dynamic Client Registration |
| **token** | **oauth** | ✅ | MCP token auth + Box OAuth |
| **token** | **ccg** | ✅ | MCP token auth + Box CCG |
| **token** | **jwt** | ✅ | MCP token auth + Box JWT |
| **token** | mcp_client | ❌ | Not supported - token requires server-side Box auth |
| **none** | **oauth** | ✅ | No MCP auth + Box OAuth |
| **none** | **ccg** | ✅ | No MCP auth + Box CCG. **Common for development** |
| **none** | **jwt** | ✅ | No MCP auth + Box JWT. **Common for development** |
| **none** | **mcp_client** | ✅ | No MCP auth. Requires Box API valid Bearer token sent in Authorization header |

## Use Cases and Recommendations

### Claude Desktop (Local Development)

**Recommended Configuration (Remote Transport):**
```bash
--transport=http --mcp-auth-type=oauth --box-auth-type=mcp_client
# or
--transport=sse --mcp-auth-type=oauth --box-auth-type=mcp_client
```

- Best user experience with OAuth flow
- MCP client handles Box OAuth configuration
- **Requires remote transport (HTTP or SSE)** - does not work with stdio

**Alternative Configuration (stdio Transport):**
```bash
--transport=stdio --mcp-auth-type=none --box-auth-type=oauth
```

- Uses stdio transport (forces `mcp-auth-type=none`)
- Server handles Box OAuth authentication
- **Note**: stdio transport is incompatible with `mcp-auth-type=oauth`

### Development and Testing

**Quick Testing (avoiding OAuth flow):**
```bash
--mcp-auth-type=none --box-auth-type=ccg
# or
--mcp-auth-type=none --box-auth-type=jwt
```

- No MCP authentication overhead
- Uses service account credentials
- **Note**: CCG and JWT require Box admin to enable the application

**Testing with User Context:**
```bash
--mcp-auth-type=none --box-auth-type=oauth
```

- Maintains user's Box security context
- Requires browser-based OAuth flow

### Production Deployment

Production deployments should consider:
1. **Transport**: Remote deployment (HTTP/SSE) is recommended
2. **User Security Context**: Whether users should have their normal Box permissions
3. **Authentication Security**: Level of authentication required between client and server

#### User-Context Authentication (Recommended for multi-user scenarios)

**Configuration:**
```bash
--transport=http --mcp-auth-type=token --box-auth-type=oauth
```

- Each user authenticates with their Box account
- Maintains individual user security contexts
- MCP server validates client access tokens
- Users can only access Box content they have permissions for

#### Service Account Authentication (For specialized agents)

**Configuration:**
```bash
--transport=http --mcp-auth-type=token --box-auth-type=ccg
# or
--transport=http --mcp-auth-type=token --box-auth-type=jwt
```

- Uses a service account with elevated permissions
- Can access Box documents that transcend user security context
- Ideal for specialized agents that need broad access
- MCP token provides security between client and server
- **Requires Box admin to enable the application**

#### Open Access with Client-Provided Box Auth

**Configuration:**
```bash
--transport=http --mcp-auth-type=none --box-auth-type=mcp_client
```

- MCP client handles all Box authentication
- Client sends Box Bearer token in Authorization header
- Flexible for various Box auth methods (developer token, OAuth, CCG, JWT)
- No authentication between MCP client and server

## Configuration Files and Environment Variables

### Environment Variables

Create a `.env` file in the project root with the appropriate configuration for your chosen authentication method.

#### For Box OAuth (`box-auth-type=oauth`)

**Example: `.env`**
```bash
BOX_CLIENT_ID = your_box_client_id
BOX_CLIENT_SECRET = your_box_client_secret
BOX_REDIRECT_URL = http://localhost:8000/callback

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

#### For Box CCG (`box-auth-type=ccg`)

CCG supports both **user** and **enterprise** (service account) authentication using `BOX_SUBJECT_TYPE` and `BOX_SUBJECT_ID`.

**Example: `.env.ccg.user` (Authenticate as a specific user)**
```bash
BOX_CLIENT_ID = your_box_client_id
BOX_CLIENT_SECRET = your_box_client_secret
BOX_SUBJECT_TYPE = user
BOX_SUBJECT_ID = your_user_id

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

**Example: `.env.ccg.enterprise` (Authenticate as service account)**
```bash
BOX_CLIENT_ID = your_box_client_id
BOX_CLIENT_SECRET = your_box_client_secret
BOX_SUBJECT_TYPE = enterprise
BOX_SUBJECT_ID = your_enterprise_id

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

**Configuration Notes:**
- `BOX_SUBJECT_TYPE`: Use `user` to authenticate as a specific Box user, or `enterprise` for service account
- `BOX_SUBJECT_ID`:
  - When `BOX_SUBJECT_TYPE=user`: Provide the Box user ID
  - When `BOX_SUBJECT_TYPE=enterprise`: Provide the Box enterprise ID

#### For Box JWT (`box-auth-type=jwt`)

JWT supports both **user** and **enterprise** (service account) authentication using `BOX_SUBJECT_TYPE` and `BOX_SUBJECT_ID`.

**Option 1: Using JWT Config File**

**Example: `.env.jwt.from.file`**
```bash
BOX_SUBJECT_TYPE = user
BOX_SUBJECT_ID = your_user_id

BOX_JWT_CONFIG_FILE = .jwt.conf.json

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

**Option 2: Using Environment Variables**

**Example: `.env.jwt.from.environment`**
```bash
BOX_CLIENT_ID = your_box_client_id
BOX_CLIENT_SECRET = your_box_client_secret
BOX_PUBLIC_KEY_ID = your_public_key_id
BOX_PRIVATE_KEY = "-----BEGIN ENCRYPTED PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END ENCRYPTED PRIVATE KEY-----\n"
BOX_PRIVATE_KEY_PASSPHRASE = your_private_key_passphrase
BOX_SUBJECT_TYPE = user
BOX_SUBJECT_ID = your_user_id

# Optional: MCP server token authentication
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token

# Optional: Logging
LOG_LEVEL = DEBUG
```

**Configuration Notes:**
- `BOX_SUBJECT_TYPE`: Use `user` to authenticate as a specific Box user, or `enterprise` for service account
- `BOX_SUBJECT_ID`:
  - When `BOX_SUBJECT_TYPE=user`: Provide the Box user ID
  - When `BOX_SUBJECT_TYPE=enterprise`: Provide the Box enterprise ID
- `BOX_PRIVATE_KEY`: Must be a quoted string with escaped newlines (`\n`)

#### For MCP Token Auth (`mcp-auth-type=token`)

The `BOX_MCP_SERVER_AUTH_TOKEN` variable is used across all Box authentication types when using `--mcp-auth-type=token`:

```bash
BOX_MCP_SERVER_AUTH_TOKEN = your_mcp_server_token
```

This token is used to authenticate the MCP client to the MCP server (independent of Box authentication).

**Important Security Note:**
Generate a strong, cryptographically secure token with at least **256 bits of entropy**. You can generate a secure token using one of these methods:

```bash
# Using OpenSSL (recommended)
openssl rand -base64 32

# Using Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

Never use predictable values, dictionary words, or short tokens for production environments.

#### OAuth Protected Resource Configuration

When using `--mcp-auth-type=oauth`, you must configure an OAuth Protected Resource metadata file that describes your MCP server to OAuth clients. This file is referenced by the `OAUTH_PROTECTED_RESOURCES_CONFIG_FILE` environment variable.

**Purpose:**

The OAuth Protected Resource configuration file provides metadata about your MCP server as an OAuth-protected resource. This allows MCP clients to discover:
- Which authorization servers can issue tokens for this resource
- What authentication methods are supported
- What scopes are available
- Where to find documentation

**Configuration:**

Create a `.oauth-protected-resource.json` file in your project root with the following structure:

```json
{
    "authorization_servers": [
        "http://localhost:8005"
    ],
    "bearer_methods_supported": [
        "header"
    ],
    "resource": "http://localhost:8005/mcp",
    "resource_documentation": "https://developer.box.com/",
    "scopes_supported": [
        "root_readonly",
        "root_readwrite",
        "manage_managed_users",
        "manage_app_users",
        "manage_groups",
        "manage_webhook",
        "manage_enterprise_properties",
        "manage_data_retention",
        "sign_requests.readwrite",
        "ai.readwrite",
        "manage_triggers"
    ]
}
```

**Field Descriptions:**

- **`authorization_servers`**: Array of authorization server URLs that can issue access tokens for this resource
  - Include your MCP server URL (e.g., `http://localhost:8005`)
  - The MCP server will still get the information from `https://account.box.com/.well-known/oauth-authorization-server` and inject the registration end point.
- **`bearer_methods_supported`**: Authentication methods supported by the resource
  - `"header"`: Bearer token sent in the Authorization header (standard for Box API)

- **`resource`**: The URL of the MCP server endpoint
  - Should match your server's base URL plus `/mcp` path for http transport and `/sse/` for SSE transport.
  - Example: `http://localhost:8005/mcp`

- **`resource_documentation`**: URL to documentation for the resource
  - Can point to Box Developer documentation or your own docs

- **`scopes_supported`**: Array of Box API scopes that this resource supports
  - List all Box OAuth scopes your application needs
  - See [Box OAuth Scopes Documentation](https://developer.box.com/guides/api-calls/permissions-and-errors/scopes/) for available scopes
  - These can more restrictive than the Box application configuration

**Environment Variable:**

Reference this file in your `.env`:

```bash
OAUTH_PROTECTED_RESOURCES_CONFIG_FILE = .oauth-protected-resource.json
```

**Important Notes:**

- This file is **only required** when using `--mcp-auth-type=oauth`
- Update `authorization_servers` and `resource` URLs to match your deployment (localhost for development, your domain for production)
- The scopes listed should match the scopes configured in your Box OAuth application
- This configuration is part of the OAuth 2.0 Protected Resource Metadata specification

### Box Application Setup

#### Creating a Box OAuth App:
1. Go to [Box Developer Console](https://app.box.com/developers/console)
2. Create a new Custom App
3. Select "User Authentication (OAuth 2.0)"
4. Configure redirect URIs
5. Copy the client ID and client secret

#### Creating a Box CCG App:
1. Go to [Box Developer Console](https://app.box.com/developers/console)
2. Create a new Custom App
3. Select "Server Authentication (Client Credentials Grant)"
4. Configure application scopes
5. Submit for admin authorization
6. Copy the client ID, client secret, and enterprise ID

#### Creating a Box JWT App:
1. Go to [Box Developer Console](https://app.box.com/developers/console)
2. Create a new Custom App
3. Select "Server Authentication (with JWT)"
4. Generate a public/private key pair
5. Submit for admin authorization
6. Download the JSON configuration file
7. Store the configuration file securely

## Security Best Practices

1. **Never commit credentials to version control**: Use `.env` files and add them to `.gitignore`
2. **Rotate tokens regularly**: Especially for production deployments
3. **Use appropriate authentication for your use case**:
   - Personal use: `oauth + mcp_client`
   - Development: `none + ccg/jwt`
   - Production (user context): `token + oauth`
   - Production (service account): `token + ccg/jwt`
4. **Restrict Box application permissions**: Only grant necessary scopes
5. **Use HTTPS in production**: For HTTP/SSE transports
6. **Implement rate limiting**: Especially for open deployments

## Troubleshooting

### "Authentication failed" errors
- Verify credentials in `.env` file
- Check Box application is authorized by admin (for CCG/JWT)
- Ensure tokens haven't expired

### "Invalid combination" errors
- Review the compatibility matrix
- Verify `mcp-auth-type` and `box-auth-type` are compatible

### OAuth redirect issues
- Check redirect URIs are configured correctly in Box app
- Ensure callback URL matches configuration

### MCP client connection issues
- For `stdio`: Verify MCP client configuration
- For HTTP/SSE: Check host and port are accessible
- Verify firewall rules allow connections

## Additional Resources

- [Box Developer Documentation](https://developer.box.com/)
- [Box OAuth 2.0 Guide](https://developer.box.com/guides/authentication/oauth2/)
- [Box CCG Guide](https://developer.box.com/guides/authentication/client-credentials/)
- [Box JWT Guide](https://developer.box.com/guides/authentication/jwt/)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
