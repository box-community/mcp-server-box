"""Authentication middleware for MCP server."""

import logging
import os

import dotenv
from fastapi import status
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from config import DEFAULT_CONFIG, TransportType
from oauth_endpoints import add_oauth_endpoints

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

    def __init__(self, app):
        self.app = app

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

        expected_token = os.getenv("BOX_MCP_SERVER_AUTH_TOKEN")

        # Extract authorization header
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("utf-8")

        # Validate authentication
        error_response = None

        if not expected_token:
            logger.error("BOX_MCP_SERVER_AUTH_TOKEN not configured")
            error_response = {
                "error": "invalid_token",
                "error_description": "Server authentication not properly configured",
            }
        elif not auth_header:
            logger.warning(f"Missing authorization header for {scope['method']} {path}")
            error_response = {
                "error": "invalid_request",
                "error_description": "Missing Authorization header",
            }
        elif not auth_header.startswith("Bearer "):
            logger.warning("Invalid authorization header format")
            error_response = {
                "error": "invalid_request",
                "error_description": "Authorization header must use Bearer scheme",
            }
        else:
            token = auth_header.replace("Bearer ", "")
            if token != expected_token:
                logger.warning(f"Invalid token for {scope['method']} {path}")
                error_response = {
                    "error": "invalid_token",
                    "error_description": "The access token is invalid or expired",
                }

        # If there's an error, send error response
        if error_response:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=error_response,
                headers=WWW_HEADER,
            )
            await response(scope, receive, send)
            return

        # Authentication successful, pass to next layer
        logger.debug(f"Authentication successful for {scope['method']} {path}")
        await self.app(scope, receive, send)


def add_auth_middleware(mcp: FastMCP, transport: str) -> None:
    """Add authentication middleware by wrapping the app creation method."""
    logger.info(f"Setting up auth middleware wrapper for transport: {transport}")

    if transport == TransportType.SSE.value:
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
            app.add_middleware(AuthMiddleware)
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
            app.add_middleware(AuthMiddleware)
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
