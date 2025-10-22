"""MCP server configuration and initialization."""

from pathlib import Path

import tomli
from mcp.server.fastmcp import FastMCP

from config import CONFIG, TransportType
from middleware import add_auth_middleware
from server_context import box_lifespan_ccg, box_lifespan_oauth
from tool_registry import register_all_tools
from tool_registry.ai_tools import register_ai_tools
from tool_registry.collaboration_tools import register_collaboration_tools
from tool_registry.doc_gen_tools import register_doc_gen_tools
from tool_registry.file_tools import register_file_tools
from tool_registry.folder_tools import register_folder_tools
from tool_registry.generic_tools import register_generic_tools
from tool_registry.group_tools import register_group_tools
from tool_registry.metadata_tools import register_metadata_tools
from tool_registry.search_tools import register_search_tools
from tool_registry.shared_link_tools import register_shared_link_tools
from tool_registry.tasks_tools import register_tasks_tools
from tool_registry.user_tools import register_user_tools
from tool_registry.web_link_tools import register_web_link_tools


def get_version() -> str:
    """Read version from pyproject.toml."""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomli.load(f)
        return pyproject_data.get("project", {}).get("version", "unknown")
    except Exception:
        return "unknown"


def create_mcp_server(
    server_name: str = CONFIG.server_name_prefix,
    transport: str = CONFIG.transport,
    host: str = CONFIG.host,
    port: int = CONFIG.port,
    box_auth: str = CONFIG.box_auth,
    require_auth: bool = True,
) -> FastMCP:
    """Create and configure the MCP server."""

    # Select appropriate lifespan based on auth type
    lifespan = box_lifespan_ccg if box_auth == "ccg" else box_lifespan_oauth

    # Create MCP server with appropriate transport
    if transport == TransportType.STDIO.value:
        mcp = FastMCP(server_name, lifespan=lifespan)
    else:
        mcp = FastMCP(
            server_name,
            stateless_http=True,
            host=host,
            port=port,
            lifespan=lifespan,
        )
        # Add authentication middleware for HTTP transports
        if require_auth:
            add_auth_middleware(mcp, transport)

    return mcp


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the MCP server."""
    register_all_tools(
        mcp,
        [
            register_generic_tools,
            register_search_tools,
            register_ai_tools,
            register_doc_gen_tools,
            register_file_tools,
            register_folder_tools,
            register_metadata_tools,
            register_user_tools,
            register_group_tools,
            register_collaboration_tools,
            register_web_link_tools,
            register_shared_link_tools,
            register_tasks_tools,
        ],
    )


def create_server_info_tool(
    mcp: FastMCP,
    transport: str,
    box_auth: str,
    host: str = "127.0.0.1",
    port: int = 8001,
) -> None:
    """Create and register the server info tool."""

    @mcp.tool()
    def mcp_server_info():
        """Returns information about the MCP server."""
        info = {
            "server_name": mcp.name,
            "version": get_version(),
            "transport": transport,
            "box auth": box_auth,
        }

        if transport != TransportType.STDIO.value:
            info["host"] = host
            info["port"] = str(port)

        return info
