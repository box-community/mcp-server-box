from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from box_ai_agents_toolkit import BoxClient, get_oauth_client
from mcp.server.fastmcp import FastMCP


@dataclass
class BoxContext:
    client: BoxClient = None


@asynccontextmanager
async def box_lifespan(server: FastMCP) -> AsyncIterator[BoxContext]:
    """Manage Box client lifecycle with OAuth handling"""
    try:
        client = get_oauth_client()
        yield BoxContext(client=client)
    finally:
        # Cleanup (if needed)
        pass