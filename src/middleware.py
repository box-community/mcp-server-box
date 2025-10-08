"""Authentication middleware for MCP server."""

import logging
import os
from typing import Literal

import dotenv
from fastapi import status
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from config import DEFAULT_CONFIG, TransportType, ServerConfig, McpAuthType
from oauth_endpoints import add_oauth_endpoints
from mcp_auth.auth_token import auth_validate_token
from mcp_auth.auth_scalekit import auth_validate_token_scalekit

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

# OAuth 2.1 configuration
WWW_HEADER = {
    "WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="http://{DEFAULT_CONFIG.host}:{DEFAULT_CONFIG.port}/.well-known/oauth-protected-resource"'
}


class AuthMiddleware:
    """Pure ASGI middleware to validate Bearer token authentication.
    Expects the token to be set in the BOX_MCP_SERVER_AUTH_TOKEN environment variable.
    This middleware wont even be loaded if the --no-mcp-server-auth flag is set.
    """

    # OAuth discovery endpoints that must be publicly accessible (no auth required)
    PUBLIC_PATHS = {
        "/.well-known/oauth-protected-resource",
        "/.well-known/oauth-protected-resource/mcp",
        "/.well-known/oauth-authorization-server",
        "/.well-known/openid-configuration",
    }

    def __init__(self, app, mcp_auth_type: str):
        self.app = app
        self.mcp_auth_type = McpAuthType(mcp_auth_type)

    async def __call__(self, scope, receive, send):
        """Pure ASGI middleware - handles streaming properly."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        logger.debug(f"AuthMiddleware processing: {scope['method']} {path}")

        # Allow public OAuth discovery endpoints without authentication
        if path in self.PUBLIC_PATHS:
            logger.debug(f"Public OAuth discovery endpoint accessed: {path}")
            await self.app(scope, receive, send)
            return

        # If no authentication required, pass through
        if self.mcp_auth_type == McpAuthType.NONE:
            logger.debug("MCP auth type is NONE, skipping authentication")
            await self.app(scope, receive, send)
            return

        error_response = None

        if self.mcp_auth_type == McpAuthType.TOKEN:
            logger.debug("MCP auth type is TOKEN, performing token authentication")
            error_response = auth_validate_token(scope=scope)

        if self.mcp_auth_type == McpAuthType.OAUTH:
            logger.debug("MCP auth type is OAUTH, performing OAuth authentication")
            error_response = await auth_validate_token_scalekit(scope=scope)

        # If there's an error, send error response
        if error_response is not None:
            # add headers to response
            error_response.headers.update(WWW_HEADER)
            await error_response(scope, receive, send)
            return

        # Authentication successful, pass to next layer
        logger.debug(
            f"[Middleware]Authentication successful for {scope['method']} {path}"
        )
        await self.app(scope, receive, send)


def add_auth_middleware(mcp: FastMCP, transport: TransportType, mcp_auth_type: McpAuthType | str) -> None:
    """Add authentication middleware by wrapping the app creation method."""
    logger.info(f"Setting up auth middleware wrapper for transport: {transport}")

    if transport == TransportType.SSE:
        # Store the original method
        original_sse_app = mcp.sse_app

        # Create a wrapper that adds middleware
        def wrapped_sse_app(mount_path: str | None = None):
            logger.info(f"wrapped_sse_app called with mount_path={mount_path}")
            app = original_sse_app(mount_path)
            logger.info(f"Adding middleware to app: {id(app)}")

            # Add OAuth discovery endpoints first
            add_oauth_endpoints(app)
            logger.info("Added OAuth discovery endpoints")

            # Then add auth middleware
            app.add_middleware(AuthMiddleware, mcp_auth_type=str(mcp_auth_type.value) if isinstance(mcp_auth_type, McpAuthType) else mcp_auth_type)
            logger.info(
                f"Middleware added. App middleware count: {len(app.user_middleware)}"
            )
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=False,
                allow_methods=["GET", "POST", "OPTIONS"],
                allow_headers=["Mcp-Protocol-Version", "Content-Type", "Authorization"],
                expose_headers=["WWW-Authenticate"],
                max_age=86400,
            )
            return app

        # Replace the method with our wrapper
        mcp.sse_app = wrapped_sse_app
        logger.info("Wrapped sse_app method")

    elif transport == TransportType.STREAMABLE_HTTP.value:
        original_streamable_http_app = mcp.streamable_http_app

        def wrapped_streamable_http_app():
            logger.info("wrapped_streamable_http_app called")
            app = original_streamable_http_app()
            logger.info(f"Adding middleware to app: {id(app)}")

            # Add OAuth discovery endpoints first
            add_oauth_endpoints(app)
            logger.info("Added OAuth discovery endpoints")

            # Then add auth middleware
            app.add_middleware(AuthMiddleware, mcp_auth_type=str(mcp_auth_type.value) if isinstance(mcp_auth_type, McpAuthType) else mcp_auth_type)
            logger.info(
                f"Middleware added. App middleware count: {len(app.user_middleware)}"
            )
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=False,
                allow_methods=["GET", "POST", "OPTIONS"],
                allow_headers=["Mcp-Protocol-Version", "Content-Type", "Authorization"],
                expose_headers=["WWW-Authenticate"],
                max_age=86400,
            )
            return app

        mcp.streamable_http_app = wrapped_streamable_http_app
        logger.info("Wrapped streamable_http_app method")
