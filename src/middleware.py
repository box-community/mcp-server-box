"""Authentication middleware for MCP server."""

import os
import logging
from fastapi import Request, HTTPException, status
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate Bearer token authentication."""

    async def dispatch(self, request: Request, call_next):
        """Validate Bearer token before processing request."""
        logger.info(f"AuthMiddleware triggered for {request.url}")
        logger.info(f"Headers: {request.headers}")

        expected_token = os.getenv("MCP_PROXY_AUTH_TOKEN")
        # logger.info(f"Expected token: {expected_token}")

        # if not expected_token:
        #     logger.info("No token configured, allowing request")
        #     return await call_next(request)

        # if no expected token is set, reject all requests
        if not expected_token:
            logger.warning("No token configured, rejecting all requests")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "No authentication token configured"},
            )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="No authentication token configured",
            # )

        auth_header = request.headers.get("authorization")
        if not auth_header:
            logger.warning("Missing authorization header")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Missing authorization header"},
            )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Missing authorization header",
            # )

        if not auth_header.startswith("Bearer "):
            logger.warning("Invalid authorization header format")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid authorization header"},
            )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Invalid authorization header",
            # )

        token = auth_header.replace("Bearer ", "")
        if token != expected_token:
            logger.warning("Invalid token")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid token"},
            )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            # )

        logger.info("Authentication successful")
        return await call_next(request)


def add_auth_middleware(mcp: FastMCP, transport: str) -> None:
    """Add authentication middleware by wrapping the app creation method."""
    logger.info(f"Setting up auth middleware wrapper for transport: {transport}")

    if transport == "sse":
        # Store the original method
        original_sse_app = mcp.sse_app

        # Create a wrapper that adds middleware
        def wrapped_sse_app(mount_path: str | None = None):
            logger.info(f"wrapped_sse_app called with mount_path={mount_path}")
            app = original_sse_app(mount_path)
            logger.info(f"Adding middleware to app: {id(app)}")
            app.add_middleware(AuthMiddleware)
            logger.info(
                f"Middleware added. App middleware count: {len(app.user_middleware)}"
            )
            return app

        # Replace the method with our wrapper
        mcp.sse_app = wrapped_sse_app
        logger.info("Wrapped sse_app method")

    elif transport == "streamable-http":
        original_streamable_http_app = mcp.streamable_http_app

        def wrapped_streamable_http_app():
            logger.info("wrapped_streamable_http_app called")
            app = original_streamable_http_app()
            logger.info(f"Adding middleware to app: {id(app)}")
            app.add_middleware(AuthMiddleware)
            logger.info(
                f"Middleware added. App middleware count: {len(app.user_middleware)}"
            )
            return app

        mcp.streamable_http_app = wrapped_streamable_http_app
        logger.info("Wrapped streamable_http_app method")
