"""Configuration for the Box MCP Server."""

from dataclasses import dataclass
from enum import Enum


class TransportType(str, Enum):
    """Available transport types for the MCP server."""

    STDIO = "stdio"
    SSE = "sse"
    STREAMABLE_HTTP = "streamable-http"


class AuthType(str, Enum):
    """Available authentication types for Box API."""

    OAUTH = "oauth"
    CCG = "ccg"


@dataclass(frozen=True)
class ServerConfig:
    """Default configuration values for the MCP server."""

    transport: str = TransportType.STDIO.value
    host: str = "0.0.0.0"
    port: int = 8001
    box_auth: str = AuthType.OAUTH.value
    require_auth: bool = True
    server_name_prefix: str = "Box Community MCP"


# Global instance
CONFIG = ServerConfig()
