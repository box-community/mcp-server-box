"""Entry point for the Box MCP Server."""

import argparse
import logging
import sys

from config import DEFAULT_CONFIG, AuthType, ServerConfig, TransportType
from server import create_mcp_server, create_server_info_tool, register_tools

# Logging configuration
logging.basicConfig(level=logging.INFO)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.INFO)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Box Community MCP Server")
    parser.add_argument(
        "--transport",
        choices=[t.value for t in TransportType],
        default=DEFAULT_CONFIG.transport,
        help=f"Transport type (default: {DEFAULT_CONFIG.transport})",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_CONFIG.host,
        help=f"Host for SSE/HTTP transport (default: {DEFAULT_CONFIG.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_CONFIG.port,
        help=f"Port for SSE/HTTP transport (default: {DEFAULT_CONFIG.port})",
    )
    parser.add_argument(
        "--box-auth",
        choices=[a.value for a in AuthType],
        default=DEFAULT_CONFIG.box_auth,
        help=f"Authentication type for Box API (default: {DEFAULT_CONFIG.box_auth})",
    )

    parser.add_argument(
        "--no-mcp-server-auth",
        action="store_true",
        help="Disable authentication (for development only)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for the Box MCP Server."""
    args = parse_arguments()

    # Create MCP server
    server_name = f"{DEFAULT_CONFIG.server_name} {args.transport.upper()} Server"

    # Create config from arguments
    config = ServerConfig(
        transport=args.transport,
        host=args.host,
        port=args.port,
        box_auth=args.box_auth,
        require_auth=not args.no_mcp_server_auth,
        server_name=server_name,
    )

    # Create and configure MCP server
    mcp = create_mcp_server(
        config=config,
    )

    # Register all tools
    register_tools(mcp)

    # Register server info tool
    create_server_info_tool(mcp, config=config)

    # Run server
    try:
        print(f"Starting {server_name} on {config.host}:{config.port}", file=sys.stderr)
        mcp.run(transport=TransportType(config.transport).value)
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
