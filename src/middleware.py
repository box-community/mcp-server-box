"""Authentication middleware for MCP server."""

import logging
import os
import json

import dotenv

from fastapi import Request, status
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from config import TransportType, DEFAULT_CONFIG

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

# OAuth 2.1 configuration
WWW_HEADER = {
    "WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="http://{DEFAULT_CONFIG.host}:{DEFAULT_CONFIG.port}/.well-known/oauth-protected-resource"'
}


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate Bearer token authentication.
    Expects the token to be set in the BOX_MCP_SERVER_AUTH_TOKEN environment variable.
    This middleware wont even be loaded if the --no-mcp-server-auth flag is set.
    """

    async def dispatch(self, request: Request, call_next):
        """Validate Bearer token before processing request according to OAuth 2.1 / RFC 9728."""
        logger.debug(f"AuthMiddleware processing: {request.method} {request.url.path}")

        expected_token = os.getenv("BOX_MCP_SERVER_AUTH_TOKEN")

        # if no expected token is set, reject all requests with proper OAuth 2.1 error
        if not expected_token:
            logger.error(
                "BOX_MCP_SERVER_AUTH_TOKEN not configured - authentication required but no token set"
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "invalid_token",
                    "error_description": "Server authentication not properly configured",
                },
                headers=WWW_HEADER,
                media_type="application/json",
            )

        auth_header = request.headers.get("authorization")
        if not auth_header:
            logger.warning(
                f"Missing authorization header for {request.method} {request.url.path}"
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "invalid_request",
                    "error_description": "Missing Authorization header",
                },
                headers=WWW_HEADER,
                media_type="application/json",
            )

        if not auth_header.startswith("Bearer "):
            logger.warning(
                f"Invalid authorization header format: {auth_header[:20]}..."
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "invalid_request",
                    "error_description": "Authorization header must use Bearer scheme",
                },
                headers=WWW_HEADER,
                media_type="application/json",
            )

        token = auth_header.replace("Bearer ", "")
        if token != expected_token:
            logger.warning(f"Invalid token for {request.method} {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "invalid_token",
                    "error_description": "The access token is invalid or expired",
                },
                headers=WWW_HEADER,
                media_type="application/json",
            )

        logger.debug(
            f"Authentication successful for {request.method} {request.url.path}"
        )
        return await call_next(request)


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
