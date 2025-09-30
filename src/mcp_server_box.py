import argparse
import logging

import tomli
from pathlib import Path
import sys

from mcp.server.fastmcp import FastMCP
from server_context import box_lifespan_ccg, box_lifespan_oauth

from tool_registry import register_all_tools
from tool_registry.ai_tools import register_ai_tools
from tool_registry.file_tools import register_file_tools
from tool_registry.folder_tools import register_folder_tools
from tool_registry.collaboration_tools import register_collaboration_tools
from tool_registry.doc_gen_tools import register_doc_gen_tools
from tool_registry.metadata_tools import register_metadata_tools
from tool_registry.search_tools import register_search_tools
from tool_registry.shared_link_tools import register_shared_link_tools
from tool_registry.user_tools import register_user_tools
from tool_registry.group_tools import register_group_tools
from tool_registry.web_link_tools import register_web_link_tools
from tool_registry.generic_tools import register_generic_tools

# Logging configuration
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)


def get_mcp_server(
    server_name: str = "Box MCP Server",
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
    auth: str = "oauth",
) -> FastMCP:
    # Initialize FastMCP server

    if auth == "ccg":
        lifespan = box_lifespan_ccg
    else:
        lifespan = box_lifespan_oauth

    if transport == "stdio":
        return FastMCP(server_name, lifespan=lifespan)
    else:
        return FastMCP(
            server_name,
            stateless_http=True,
            host=host,
            port=port,
            lifespan=lifespan,
        )


def create_server_info_tool(mcp: FastMCP, args):
    """Create and register the server info tool"""

    def get_version():
        """Read version from pyproject.toml"""
        try:
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
            return pyproject_data.get("project", {}).get("version", "unknown")
        except Exception:
            return "unknown"

    @mcp.tool()
    def mcp_server_info():
        """Returns information about the MCP server."""
        info = {
            "server_name": mcp.name,
            "version": get_version(),
            "transport": args.transport,
            "auth": args.auth,
        }

        if args.transport != "stdio":
            info["host"] = args.host
            info["port"] = args.port

        return info


def main():
    """Main entry point for the Box MCP Server."""
    parser = argparse.ArgumentParser(description="Box Community MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE/HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE/HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth",
        choices=["oauth", "ccg"],
        default="oauth",
        help="Authentication type (default: oauth)",
    )

    args = parser.parse_args()

    # Initialize FastMCP server
    mcp = get_mcp_server(
        server_name=f"Box Community MCP {args.transport.upper()} Server",
        transport=args.transport,
        host=args.host,
        port=args.port,
        auth=args.auth,
    )

    # Register all tools
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
        ],
    )

    # Register server info tool
    create_server_info_tool(mcp, args)

    # Run server
    try:
        mcp.run(transport=args.transport)
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
