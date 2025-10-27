from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator
import logging

from box_ai_agents_toolkit import BoxClient, get_ccg_client
from box_sdk_gen import BoxDeveloperTokenAuth
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request

logger = logging.getLogger(__name__)


@dataclass
class BoxContext:
    client: BoxClient | None = None
    request: Request | None = None

    def get_client_with_token(self, token: str) -> BoxClient:
        """Create a Box client using the provided OAuth token."""
        logger.info("Creating Box client with OAuth token")
        auth = BoxDeveloperTokenAuth(token=token)
        return BoxClient(auth=auth)

    def get_active_client(self) -> BoxClient:
        """Get the active Box client.

        For OAuth mode: extracts the token from the request and creates a client.
        For CCG mode: returns the pre-created client.

        Raises:
            ValueError: If no client is available or no OAuth token found.
        """
        # If we have a pre-created client (CCG mode), use it
        if self.client is not None:
            logger.debug("Using pre-created Box client (CCG mode)")
            return self.client

        # OAuth mode: extract token from request scope
        if self.request is None:
            raise ValueError("No request context available")

        # Get the OAuth token from the request scope (set by middleware)
        token = self.request.scope.get("oauth_token")
        if not token:
            raise ValueError("No OAuth token found in request scope")

        logger.debug("Creating Box client from request OAuth token")
        return self.get_client_with_token(token)


@asynccontextmanager
async def box_lifespan_oauth(server: FastMCP) -> AsyncIterator[BoxContext]:
    """Manage Box client lifecycle with OAuth handling.

    In OAuth mode, the client is created per-request using the Bearer token
    from the Authorization header. The middleware stores the token in the
    request scope, and tools should use context.get_client_with_token() to
    create the client dynamically.
    """
    try:
        # Don't create a client at startup - it will be created per-request
        logger.info("OAuth mode: Box client will be created per-request from Bearer token")
        yield BoxContext(client=None)
    finally:
        # Cleanup (if needed)
        pass


@asynccontextmanager
async def box_lifespan_ccg(server: FastMCP) -> AsyncIterator[BoxContext]:
    """Manage Box client lifecycle with CCG handling"""
    try:
        client = get_ccg_client()
        yield BoxContext(client=client)
    finally:
        # Cleanup (if needed)
        pass
