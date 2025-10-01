"""Entry point for the Box MCP Server."""

import argparse
import logging
import sys

from server import create_mcp_server, register_tools, create_server_info_tool


# Logging configuration
logging.basicConfig(level=logging.INFO)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.INFO)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
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
        default=8001,
        help="Port for SSE/HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--box-auth",
        choices=["oauth", "ccg"],
        default="oauth",
        help="Authentication type for Box API (default: oauth)",
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
    server_name = f"Box Community MCP {args.transport.upper()} Server"
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
