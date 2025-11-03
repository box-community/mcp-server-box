"""Entry point for the Box MCP Server."""

import argparse
import logging
import sys

from config import (
    AppConfig,
    BoxAuthType,
    McpAuthType,
    TransportType,
    setup_logging,
)
from server import create_mcp_server, create_server_info_tool, register_tools

# Load configuration from environment once at startup
app_config = AppConfig.from_env()

# Configure logging
setup_logging(app_config.logging.log_level)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Box Community MCP Server")
    parser.add_argument(
        "--transport",
        choices=[t.value for t in TransportType],
        default=app_config.server.transport,
        help=f"Transport type (default: {app_config.server.transport.value})",
    )
    parser.add_argument(
        "--host",
        default=app_config.server.host,
        help=f"Host for SSE/HTTP transport (default: {app_config.server.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=app_config.server.port,
        help=f"Port for SSE/HTTP transport (default: {app_config.server.port})",
    )

    parser.add_argument(
        "--mcp-auth-type",
        choices=[a.value for a in McpAuthType],
        default=app_config.server.mcp_auth_type,
        help=f"Authentication type for MCP server (default: {app_config.server.mcp_auth_type.value})",
    )

    parser.add_argument(
        "--box-auth-type",
        choices=[a.value for a in BoxAuthType],
        default=app_config.server.box_auth,
        help=f"Authentication type for Box API (default: {app_config.server.box_auth.value})",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for the Box MCP Server."""
    args = parse_arguments()

    # Update server config from command line arguments
    app_config.server.transport = TransportType(args.transport)
    app_config.server.host = args.host
    app_config.server.port = args.port
    app_config.server.box_auth = args.box_auth_type
    app_config.server.mcp_auth_type = args.mcp_auth_type

    # Validate and adjust config based on transport type
    # if the transport is stdio, then the mcp auth must be none
    if app_config.server.transport == TransportType.STDIO:
        if app_config.server.mcp_auth_type != McpAuthType.NONE:
            logger.warning(
                "MCP auth type must be 'none' when using stdio transport. Overriding to 'none'."
            )
        app_config.server.mcp_auth_type = McpAuthType.NONE

    if app_config.server.mcp_auth_type == McpAuthType.OAUTH:
        if app_config.server.box_auth != BoxAuthType.MCP_CLIENT:
            logger.warning(
                "Box auth type must be 'mcp_client' when using MCP OAuth authentication. Overriding to 'mcp_client'."
            )
        app_config.server.box_auth = BoxAuthType.MCP_CLIENT

    # Create and configure MCP server
    mcp = create_mcp_server(
        app_config=app_config,
    )

    # Register all tools
    register_tools(mcp)

    # Register server info tool
    create_server_info_tool(mcp, config=app_config.server)

    # Run server
    try:
        logger.info(f"Starting {app_config.server.server_name}")
        if app_config.server.transport != TransportType.STDIO:
            logger.info(f"Listening on {app_config.server.host}:{app_config.server.port}")
        transport_value = app_config.server.transport.value
        if transport_value == "http":
            transport_value = "streamable-http"
        mcp.run(transport=transport_value)
        return 0
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
