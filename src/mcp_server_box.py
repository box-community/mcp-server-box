"""Entry point for the Box MCP Server."""

import argparse
import logging
import sys

from config import (
    DEFAULT_CONFIG,
    BoxAuthType,
    McpAuthType,
    ServerConfig,
    TransportType,
    setup_logging,
)
from server import create_mcp_server, create_server_info_tool, register_tools

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Box Community MCP Server")
    parser.add_argument(
        "--transport",
        choices=[t.value for t in TransportType],
        default=DEFAULT_CONFIG.transport,
        help=f"Transport type (default: {DEFAULT_CONFIG.transport.value})",
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
        "--box-auth-type",
        choices=[a.value for a in BoxAuthType],
        default=DEFAULT_CONFIG.box_auth,
        help=f"Authentication type for Box API (default: {DEFAULT_CONFIG.box_auth.value})",
    )

    parser.add_argument(
        "--mcp-auth-type",
        choices=[a.value for a in McpAuthType],
        default=DEFAULT_CONFIG.mcp_auth_type,
        help=f"Authentication type for MCP server (default: {DEFAULT_CONFIG.mcp_auth_type.value})",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for the Box MCP Server."""
    args = parse_arguments()

    # Create MCP server
    server_name = f"{DEFAULT_CONFIG.server_name} {args.transport.upper()} Server"

    # Create config from arguments
    config = ServerConfig(
        transport=TransportType(args.transport),
        host=args.host,
        port=args.port,
        box_auth=args.box_auth_type,
        mcp_auth_type=args.mcp_auth_type,
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
        logger.info(f"Starting {server_name}")
        if config.transport != TransportType.STDIO:
            logger.info(f"Listening on {config.host}:{config.port}")
        transport_value = config.transport.value
        if transport_value == "http":
            transport_value = "streamable-http"
        mcp.run(transport=transport_value)
        return 0
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
