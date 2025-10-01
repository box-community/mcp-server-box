"""Entry point for the Box MCP Server."""

import argparse
import logging
import sys

from config import CONFIG, AuthType, TransportType
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
        default=CONFIG.transport,
        help=f"Transport type (default: {CONFIG.transport})",
    )
    parser.add_argument(
        "--host",
        default=CONFIG.host,
        help=f"Host for SSE/HTTP transport (default: {CONFIG.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=CONFIG.port,
        help=f"Port for SSE/HTTP transport (default: {CONFIG.port})",
    )
    parser.add_argument(
        "--box-auth",
        choices=[a.value for a in AuthType],
        default=CONFIG.box_auth,
        help=f"Authentication type for Box API (default: {CONFIG.box_auth})",
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
    server_name = f"{CONFIG.server_name_prefix} {args.transport.upper()} Server"
    mcp = create_mcp_server(
        server_name=server_name,
        transport=args.transport,
        host=args.host,
        port=args.port,
        box_auth=args.box_auth,
        require_auth=not args.no_mcp_server_auth,
    )

    # Register all tools
    register_tools(mcp)

    # Register server info tool
    create_server_info_tool(mcp, args.transport, args.box_auth, args.host, args.port)

    # Run server
    try:
        print(f"Starting {server_name} on {args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport=args.transport)
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
