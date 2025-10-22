# Box MCP Server

## Quick Start

### Clone the repository:

```sh
git clone https://github.com/box-community/mcp-server-box.git
cd mcp-server-box
```

### Optional but recommended `uv` installation for virtual environment and dependency management:

#### Homebrew (macOS)
```sh
brew install uv
```

#### WinGet (Windows)
```sh
winget install --id=astral-sh.uv  -e
```

#### On macOS and Linux
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### On Windows
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Set up the virtual environment and install dependencies:

```sh
uv sync
```

### Set environment variables:
Set the following environment variables for Box authentication in a `.env` file or your system environment:

#### Using OAuth2.0 with a Box App
```
BOX_CLIENT_ID = YOUR_CLIENT_ID
BOX_CLIENT_SECRET = YOUR_CLIENT_SECRET
BOX_REDIRECT_URL = http://localhost:8000/callback

BOX_MCP_SERVER_AUTH_TOKEN = YOUR_BOX_MCP_SERVER_AUTH_TOKEN
```

#### Using CCG with a Box App
```
BOX_CLIENT_ID = YOUR_CLIENT_ID
BOX_CLIENT_SECRET = YOUR_CLIENT_SECRET
BOX_SUBJECT_TYPE = user_or_enterprise
BOX_SUBJECT_ID = YOUR_USER_OR_ENTERPRISE_ID

BOX_MCP_SERVER_AUTH_TOKEN = YOUR_BOX_MCP_SERVER_AUTH_TOKEN
```

> Note: The `BOX_MCP_SERVER_AUTH_TOKEN` is the token used to authenticate requests to the Box MCP server. You can generate this token.

### Run the MCP server in STDIO mode:
```sh
uv run src/mcp_server_box.py
```

## Box Community MCP Server Tools

Below is a summary of the available tools:

| Tools available          | Description                                      |
|--------------------------|--------------------------------------------------|
| [box_tools_ai](docs/box_tools_ai.md) | AI-powered file and hub queries                  |
| [box_tools_collaboration](docs/box_tools_collaboration.md)  | Manage file/folder collaborations                |
| [box_tools_docgen](docs/box_tools_docgen.md)         | Document generation and template management      |
| [box_tools_files](docs/box_tools_files.md)          | File operations (read, upload, download)         |
| [box_tools_folders](docs/box_tools_folders.md)        | Folder operations (list, create, delete, update) |
| [box_tools_generic](docs/box_tools_generic.md)        | Generic Box API utilities                        |
| [box_tools_groups](docs/box_tools_groups.md)         | Group management and queries                     |
| [box_tools_metadata](docs/box_tools_metadata.md)       | Metadata template and instance management        |
| [box_tools_search](docs/box_tools_search.md)         | Search files and folders                         |
| [box_tools_shared_links](docs/box_tools_shared_links.md)   | Shared link management for files/folders/web-links|
| [box_tools_tasks](docs/box_tools_tasks.md)          | Task and task assignment management              |
| [box_tools_users](docs/box_tools_users.md)          | User management and queries                      |
| [box_tools_web_link](docs/box_tools_web_link.md)       | Web link creation and management                 |

## Box Community MCP Server Operations Details

### Command line interface parameters
To run the MCP server with specific configurations, you can use the following command line parameters:
```sh
uv run src/mcp_server_box.py --help
```
```
usage: mcp_server_box.py [-h] [--transport {stdio,sse,streamable-http}] [--host HOST]
                         [--port PORT] [--box-auth {oauth,ccg}] [--no-mcp-server-auth]

Box Community MCP Server

options:
  -h, --help            show this help message and exit
  --transport {stdio,sse,streamable-http}
                        Transport type (default: stdio)
  --host HOST           Host for SSE/HTTP transport (default: 0.0.0.0)
  --port PORT           Port for SSE/HTTP transport (default: 8000)
  --box-auth {oauth,ccg}
                        Authentication type for Box API (default: oauth)
  --no-mcp-server-auth  Disable authentication (for development only)
  ```

### Claude Desktop Configuration
Edit your `claude_desktop_config.json`:

```code ~/Library/Application\ Support/Claude/claude_desktop_config.json```

Add the configuration:
```json
{
    "mcpServers": {
        "mcp-server-box": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/mcp-server-box",
                "run",
                "src/mcp_server_box.py"
            ]
        }
    }
}
```

Restart Claude if it is running.

### Cursor Configuration

Cursor supports MCP servers through its configuration file. Here's how to set it up:

The Cursor MCP configuration file is located at:
- **macOS/Linux**: `~/.cursor/config.json` or `~/.config/cursor/config.json`
- **Windows**: `%APPDATA%\Cursor\config.json`

#### Add the MCP Server Configuration: STDIO Transport

Edit your Cursor configuration file and add the following under the `mcpServers` section:
```json
{
    "mcpServers": {
        "mcp-server-box": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/mcp-server-box",
                "run",
                "src/mcp_server_box.py"
            ],
            "env": {
                "BOX_CLIENT_ID": "YOUR_CLIENT_ID",
                "BOX_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
                "BOX_REDIRECT_URL": "http://localhost:8000/callback"
            }
        }
    }
}