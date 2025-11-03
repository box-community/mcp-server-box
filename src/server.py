"""MCP server configuration and initialization."""

from pathlib import Path

import tomli
from mcp.server.fastmcp import FastMCP

from config import AppConfig, ServerConfig, TransportType
from middleware import add_auth_middleware
from server_context import (
    box_lifespan_ccg,
    box_lifespan_jwt,
    box_lifespan_mcp_oauth,
    box_lifespan_oauth,
)
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
    app_config: AppConfig,
) -> FastMCP:
    """
    Create and configure the MCP server.

    Args:
        app_config: Complete application configuration

    Returns:
        FastMCP: Configured MCP server instance
    """

    # Select appropriate lifespan based on auth type
    if app_config.server.box_auth == "oauth":
        def lifespan(server):
            return box_lifespan_oauth(server, app_config.box_api)
    elif app_config.server.box_auth == "ccg":
        def lifespan(server):
            return box_lifespan_ccg(server, app_config.box_api)
    elif app_config.server.box_auth == "jwt":
        def lifespan(server):
            return box_lifespan_jwt(server, app_config.box_api)
    elif app_config.server.box_auth == "mcp_client":
        lifespan = box_lifespan_mcp_oauth
    else:
        raise ValueError(f"Unsupported Box auth type: {app_config.server.box_auth}")

    # Create MCP server with appropriate transport
    if app_config.server.transport == TransportType.STDIO.value:
        mcp = FastMCP(name=app_config.server.server_name, lifespan=lifespan)
    else:
        mcp = FastMCP(
            name=app_config.server.server_name,
            stateless_http=True,
            host=app_config.server.host,
            port=app_config.server.port,
            lifespan=lifespan,
        )
        # Add authentication middleware for HTTP/SSE transports
        add_auth_middleware(mcp, app_config)

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
    config: ServerConfig,
) -> None:
    """Create and register the server info tool."""

    @mcp.tool()
    def mcp_server_info():
        """Returns information about the MCP server."""
        info = {
            "server_name": mcp.name,
            "version": get_version(),
            "transport": config.transport,
            "mcp auth": config.mcp_auth_type,
            "box auth": config.box_auth,
        }

        if config.transport != TransportType.STDIO.value:
            info["host"] = config.host
            info["port"] = str(config.port)

        return info
